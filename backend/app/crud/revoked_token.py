"""CRUD utilities for RevokedToken model."""

from datetime import datetime
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.revoked_token import RevokedToken

async def is_revoked(db: AsyncSession, jti: str) -> bool:
    result = await db.execute(select(RevokedToken).where(RevokedToken.jti == jti))
    token = result.scalars().first()
    return token is not None

async def revoke(db: AsyncSession, jti: str, expires_at: datetime):
    token = RevokedToken(jti=jti, expires_at=expires_at)
    db.add(token)
    await db.commit()

async def prune_expired(db: AsyncSession):
    await db.execute(delete(RevokedToken).where(RevokedToken.expires_at < datetime.utcnow()))
    await db.commit()
