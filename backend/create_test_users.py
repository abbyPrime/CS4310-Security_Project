"""
Script to create test users and assign roles.
Idempotent — safe to run multiple times.
"""
from database import Sessionlocal
from models import User, Production, UserProduction, Role, UserRole
from auth import hash_password


TEST_USERS = [
    {"username": "testuser", "password": "password123", "role": "screenwriter"},
    {"username": "admin",    "password": "admin123",    "role": "producer"},
    {"username": "demo",     "password": "demo123",     "role": "actor"},
]

ROLE_NAMES = ["screenwriter", "producer", "actor", "director"]


def create_test_users():
    db = Sessionlocal()
    try:
        # Ensure production exists
        production = db.query(Production).first()
        if not production:
            production = Production(name="Test Movie Production")
            db.add(production)
            db.flush()
            print(f"✓ Created production: {production.name}")
        else:
            print(f"✓ Production exists: {production.name}")

        # Ensure all roles exist for the production
        roles = {}
        for role_name in ROLE_NAMES:
            role = db.query(Role).filter(
                Role.production_id == production.production_id,
                Role.role_name == role_name
            ).first()
            if not role:
                role = Role(production_id=production.production_id, role_name=role_name)
                db.add(role)
                db.flush()
                print(f"✓ Created role: {role_name}")
            roles[role_name] = role

        # Ensure users exist and have roles assigned
        for user_data in TEST_USERS:
            user = db.query(User).filter(User.username == user_data["username"]).first()
            if not user:
                hashed, salt = hash_password(user_data["password"])
                user = User(username=user_data["username"], password_hash=hashed, salt=salt)
                db.add(user)
                db.flush()
                print(f"✓ Created user: {user_data['username']}")
            else:
                print(f"✓ User exists: {user_data['username']}")

            # Assign to production if not already
            up = db.query(UserProduction).filter(
                UserProduction.user_id == user.user_id,
                UserProduction.production_id == production.production_id
            ).first()
            if not up:
                db.add(UserProduction(user_id=user.user_id, production_id=production.production_id))

            # Assign role if not already
            role = roles[user_data["role"]]
            ur = db.query(UserRole).filter(
                UserRole.user_id == user.user_id,
                UserRole.role_id == role.role_id
            ).first()
            if not ur:
                db.add(UserRole(user_id=user.user_id, role_id=role.role_id))
                print(f"  → Assigned role '{user_data['role']}' to {user_data['username']}")

        db.commit()
        print("\n✅ Test users and roles ready!")
        print("\nCredentials:")
        for u in TEST_USERS:
            print(f"  {u['username']} / {u['password']}  [{u['role']}]")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()
