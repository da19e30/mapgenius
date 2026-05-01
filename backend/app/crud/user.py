"""CRUD utilities for the User model."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str, full_name: str | None = None, role: str = "accountant") -> User:
    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed, full_name=full_name, role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
