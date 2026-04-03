"""
Script to initialize the database tables.
Run this script from the backend directory:
    python init_db.py
"""
from database import Base, engine
from models import User, Production, UserProduction, Role, UserRole


def init_database():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("  - users")
        print("  - productions")
        print("  - user_productions")
        print("  - roles")
        print("  - user_roles")
        print("\nNext step: Run 'python create_test_users.py' to create test users")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    init_database()
