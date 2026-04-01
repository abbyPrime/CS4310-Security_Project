from pydantic import BaseModel
from typing import List


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProductionBase(BaseModel):
    production_id: int
    name: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    username: str
    productions: List[ProductionBase] = []

    class Config:
        from_attributes = True
