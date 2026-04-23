from flask import Flask, request, send_file, session, abort
import psycopg2
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


@app.route("/download_screenplay")
def download_screenplay():
    # ✅ Step 1: Get logged-in user
    user_id = session.get("user_id")
    if not user_id:
        abort(401, "User not logged in")

    # ✅ Step 2: Get screenplay ID from request
    screenplay_id = request.args.get("screenplay_id")
    if not screenplay_id:
        abort(400, "Missing screenplay_id")

    conn = get_db_connection()

    try:
        # ✅ Step 3: Run your filtering logic
        filtered_lines = filter_screenplay(conn, user_id, int(screenplay_id))

        # ✅ Step 4: Write to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        with open(temp_file.name, "w", encoding="utf-8") as f:
            for line in filtered_lines:
                f.write(line + "\n")

        # ✅ Step 5: Send file as download
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name="screenplay.txt",
            mimetype="text/plain"
        )

    finally:
        conn.close()


# IMPORTANT: include your previously defined filter_screenplay() here