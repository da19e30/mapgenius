"""Pydantic schemas for user‑related requests and responses."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    accountant = "accountant"
    viewer = "viewer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: Role = Role.accountant

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
