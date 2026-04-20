"""
Script to initialize the database tables.
Run this script from the backend directory:
    python init_db.py
"""
import os
from database import engine
from sqlalchemy import text


def init_database():
    print("Creating database tables from schema.sql...")
    try:
        # Read the schema.sql file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()

            # Execute the SQL schema
            with engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
                for statement in statements:
                    try:
                        conn.execute(text(statement))
                    except Exception as stmt_error:
                        # Skip if table already exists
                        if 'already exists' not in str(stmt_error):
                            print(f"Warning: {stmt_error}")
                conn.commit()

            print("✅ Database tables created successfully from schema.sql!")
            print("\nCreated tables:")
            print("  - users")
            print("  - productions")
            print("  - user_productions")
            print("  - roles")
            print("  - user_roles")
            print("  - screenplays")
            print("  - screenplay_lines")
            print("  - line_permissions")
            print("  - comments")
            print("  - messages")
            print("\nNext step: Run 'python create_test_users.py' to create test users")
        else:
            print(f"❌ schema.sql not found at {schema_path}")
            print("Falling back to SQLAlchemy models...")
            from models import User, Production, UserProduction, Role, UserRole
            from database import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Basic tables created from models")

    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    init_database()
