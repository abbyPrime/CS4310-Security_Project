import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, request, send_file, session, abort
import tempfile

app = Flask(__name__)
app.secret_key = "your_secret_key"


def get_db_connection():
    return psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port=5432
    )


@app.route("/api/download_filtered/<int:screenplay_id>", methods=["GET"])
def download_screenplay(screenplay_id):

    user_id = 1  # replace with real auth

    conn = get_db_connection()

    try:
        filtered_lines = filter_screenplay(conn, user_id, screenplay_id)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")

        with open(temp_file.name, "w", encoding="utf-8") as f:
            for line in filtered_lines:
                f.write(line + "\n")

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name="screenplay.txt",
            mimetype="text/plain"
        )

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}, 500

    finally:
        conn.close()



def get_user_roles(conn, user_id, production_id):
    """
    Get all role_ids for a user within a production.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT r.role_id
            FROM user_roles ur
            JOIN roles r ON ur.role_id = r.role_id
            WHERE ur.user_id = %s
              AND r.production_id = %s
        """, (user_id, production_id))

        return {row[0] for row in cur.fetchall()}


def get_screenplay_lines(conn, screenplay_id):
    """
    Fetch all lines for a screenplay.
    """
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT line_id, line_number, encrypted_content
            FROM screenplay_lines
            WHERE screenplay_id = %s
            ORDER BY line_number
        """, (screenplay_id,))

        return cur.fetchall()


def get_line_permissions(conn, screenplay_id):
    """
    Map line_id -> set(role_id) that can view it.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT lp.line_id, lp.role_id
            FROM line_permissions lp
            JOIN screenplay_lines sl ON lp.line_id = sl.line_id
            WHERE sl.screenplay_id = %s
        """, (screenplay_id,))

        permissions = {}
        for line_id, role_id in cur.fetchall():
            permissions.setdefault(line_id, set()).add(role_id)

        return permissions


def get_production_id(conn, screenplay_id):
    """
    Get production_id for a screenplay.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT production_id
            FROM screenplays
            WHERE screenplay_id = %s
              AND is_revoked = FALSE
        """, (screenplay_id,))

        result = cur.fetchone()
        if not result:
            raise ValueError("Invalid or revoked screenplay")

        return result[0]


def user_in_production(conn, user_id, production_id):
    """
    Verify user belongs to production.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1
            FROM user_productions
            WHERE user_id = %s AND production_id = %s
        """, (user_id, production_id))

        return cur.fetchone() is not None


def filter_screenplay(conn, user_id, screenplay_id):
    """
    Core logic: returns filtered screenplay lines.
    """

    # Step 1: Validate screenplay + get production
    production_id = get_production_id(conn, screenplay_id)

    # Step 2: Ensure user belongs to production
    if not user_in_production(conn, user_id, production_id):
        raise PermissionError("User not part of this production")

    # Step 3: Get user roles
    user_roles = get_user_roles(conn, user_id, production_id)

    # Step 4: Get screenplay lines
    lines = get_screenplay_lines(conn, screenplay_id)

    # Step 5: Get permissions
    permissions = get_line_permissions(conn, screenplay_id)

    # Step 6: Filter lines
    output = []

    for line in lines:
        line_id = line["line_id"]
        line_number = line["line_number"]
        content = line["encrypted_content"]  # assume already decrypted or plaintext

        allowed_roles = permissions.get(line_id, set())

        # If no permissions defined → default deny
        if not allowed_roles:
            output.append(f"{line_number}: [REDACTED]")
            continue

        # Check intersection
        if user_roles.intersection(allowed_roles):
            output.append(f"{line_number}: {content}")
        else:
            output.append(f"{line_number}: [REDACTED]")

    return output


def export_screenplay(conn, user_id, screenplay_id, output_file):
    """
    Writes filtered screenplay to file.
    """
    filtered_lines = filter_screenplay(conn, user_id, screenplay_id)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in filtered_lines:
            f.write(line + "\n")


# -------------------------
# Example Usage
# -------------------------

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port=5432
    )

    try:
        user_id = 1
        screenplay_id = 5

        export_screenplay(
            conn,
            user_id,
            screenplay_id,
            "filtered_script.txt"
        )

        print("Filtered screenplay exported.")

    finally:
        conn.close()