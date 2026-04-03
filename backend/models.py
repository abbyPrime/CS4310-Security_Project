from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
