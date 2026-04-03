import hashlib
import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str, salt: str = "") -> bool:
    """
    Verify a password against its hash using SHA-256 with salt.
    Note: For production, consider using bcrypt or argon2 instead.
    """
    # Hash the plain password with salt
    password_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
    return password_hash == hashed_password


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hash a password using SHA-256 with salt.
    Returns (hash, salt) tuple.
    """
    if salt is None:
        salt = os.urandom(32).hex()

    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt
