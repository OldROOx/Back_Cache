from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginDTO(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TokenDTO(BaseModel):
    access_token: str
    token_type: str