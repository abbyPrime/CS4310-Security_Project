from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import RegisterRequest, RegisterResponse
from auth import hash_password

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Hash password server-side
    hashed_password = hash_password(request.password)

    # Create new user
    new_user = User(
        username=request.username,
        password_hash=hashed_password,
        salt="bcrypt_internal",  # bcrypt handles salt internally
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterResponse(user_id=new_user.user_id, username=new_user.username)
