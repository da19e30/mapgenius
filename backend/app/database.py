"""Database utilities for Mapgenius Solutions.

This module configures a SQLAlchemy engine with connection pooling, integrates
pgbouncer compatibility, and provides a simple health‑check function that can
be used by an HTTP endpoint.
"""

import os
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

# ---------------------------------------------------------------------------
# Engine configuration
# ---------------------------------------------------------------------------
# DATABASE_URL must be provided via environment variable. It should be in the
# ``postgresql+psycopg2`` format. Example:
#   export DATABASE_URL="postgresql+psycopg2://app_user:pwd@db-host:5432/mapgenius"
#
# ``pool_pre_ping`` ensures that stale connections are validated before use –
# important when a connection pool sits behind pgBouncer which may close idle
# connections.
# ``pool_size`` and ``max_overflow`` are tuned for typical SaaS traffic; they
# can be overridden with env vars for flexibility.
# ---------------------------------------------------------------------------
_DATABASE_URL = os.getenv("DATABASE_URL")
if not _DATABASE_URL:
    _DATABASE_URL = "sqlite:///mapgenius.db"

_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))

engine: Engine = create_engine(
    _DATABASE_URL,
    pool_size=_POOL_SIZE,
    max_overflow=_MAX_OVERFLOW,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def get_engine() -> Engine:
    """Return the configured SQLAlchemy engine.

    Keeping this function allows other modules to import ``engine`` lazily
    without creating circular import issues.
    """
    return engine

def health_check() -> dict[str, Any]:
    """Perform a lightweight DB health check.

    The function executes ``SELECT 1`` and returns a JSON‑serialisable dict
    indicating the status. It catches connection errors and translates them
    into a failure payload suitable for an HTTP ``/health/db`` endpoint.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "details": "connection successful"}
    except OperationalError as exc:
        return {"status": "error", "details": str(exc)}

def get_db():
    """Generador de sesión de base de datos para usar con Depends de FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Crear todas las tablas definidas en los modelos (si no existen)."""
    import app.models.user  # Importa modelos para que estén registrados
    Base.metadata.create_all(bind=engine)
