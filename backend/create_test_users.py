"""
Script to create test users in the database.
Run this script from the backend directory:
    python create_test_users.py
"""
from database import Sessionlocal
from models import User, Production, UserProduction
from auth import hash_password


def create_test_users():
    db = Sessionlocal()
    try:
        # Check if test users already exist
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("Test users already exist!")
            return

        # Create test users
        test_users = [
            {"username": "testuser", "password": "password123"},
            {"username": "admin", "password": "admin123"},
            {"username": "demo", "password": "demo123"},
        ]

        created_users = []
        for user_data in test_users:
            # Hash password with salt
            hashed_password, salt = hash_password(user_data["password"])

            # Create user
            new_user = User(
                username=user_data["username"],
                password_hash=hashed_password,
                salt=salt,
            )
            db.add(new_user)
            db.flush()  # Flush to get the user_id
            created_users.append(new_user)
            print(f"✓ Created user: {user_data['username']} (password: {user_data['password']})")

        # Create a test production
        test_production = Production(
            name="Test Movie Production"
        )
        db.add(test_production)
        db.flush()
        print(f"\n✓ Created production: {test_production.name}")

        # Assign first user to the production
        if created_users:
            user_production = UserProduction(
                user_id=created_users[0].user_id,
                production_id=test_production.production_id
            )
            db.add(user_production)
            print(f"✓ Assigned {created_users[0].username} to production")

        db.commit()
        print("\n✅ Test users created successfully!")
        print("\nYou can now login with:")
        for user_data in test_users:
            print(f"  - Username: {user_data['username']}, Password: {user_data['password']}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test users: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating test users...\n")
    create_test_users()
