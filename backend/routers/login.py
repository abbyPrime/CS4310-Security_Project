from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserProduction, Production, UserRole, Role
from schemas import LoginRequest, LoginResponse
from auth import verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Verify password
    if not verify_password(request.password, user.password_hash, user.salt):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Fetch user's productions
    productions = (
        db.query(Production)
        .join(UserProduction, UserProduction.production_id == Production.production_id)
        .filter(UserProduction.user_id == user.user_id)
        .all()
    )

    # Get user's role
    user_role = (
        db.query(Role)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user.user_id)
        .first()
    )
    role_name = user_role.role_name if user_role else "viewer"

    # Generate JWT token including production ids and role
    production_ids = [p.production_id for p in productions]
    token = create_access_token(
        data={"sub": str(user.user_id), "productions": production_ids, "role": role_name}
    )

    return LoginResponse(access_token=token)
