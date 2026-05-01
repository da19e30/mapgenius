"""Database engine and async session factory.

Uses the DATABASE_URL from settings. In development we run PostgreSQL via Docker Compose.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Async PostgreSQL driver – asyncpg
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Session maker for dependencies
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
