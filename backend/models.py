from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    productions = relationship("UserProduction", back_populates="user")


class Production(Base):
    __tablename__ = "productions"

    production_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    users = relationship("UserProduction", back_populates="production")


class UserProduction(Base):
    __tablename__ = "user_productions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    production_id = Column(
        Integer, ForeignKey("productions.production_id"), primary_key=True
    )

    user = relationship("User", back_populates="productions")
    production = relationship("Production", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    production_id = Column(
        Integer, ForeignKey("productions.production_id"), nullable=False
    )
    role_name = Column(String(100), nullable=False)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    file_id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    is_revoked = Column(Boolean, default=False)

    uploader = relationship("User")
