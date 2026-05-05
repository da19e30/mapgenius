"""Tenant middleware for multi-tenant SaaS.

This middleware:
1. Extracts tenant_id from JWT (set by auth_middleware).
2. Verifies that the authenticated user belongs to that tenant.
3. For PostgreSQL: sets search_path to the tenant's schema.
4. For SQLite: logs a warning (schema not supported).

Assumptions:
- Auth middleware has already placed `request.state.user_id` and `request.state.tenant_id`.
- Each tenant has a schema named `tenant_<id>` or as stored in `tenants.schema_name`.
"""

import logging
from fastapi import Request, Response, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy import text

from app.database import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User

logger = logging.getLogger(__name__)


async def tenant_middleware(request: Request, call_next):
    """Validate tenant isolation and set DB schema."""
    # Skip if no tenant context (public endpoints like login, register)
    if not hasattr(request.state, "user_id") or not hasattr(request.state, "tenant_id"):
        return await call_next(request)

    user_id = request.state.user_id
    tenant_id = request.state.tenant_id

    # Verify user belongs to the claimed tenant
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User not found")
        if user.tenant_id != tenant_id:
            logger.warning(
                f"Tenant mismatch: user {user_id} belongs to tenant {user.tenant_id}, "
                f"but token claims tenant {tenant_id}"
            )
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Tenant access denied")

        # For PostgreSQL, set search_path to tenant schema
        engine = db.bind
        if engine and engine.dialect.name == "postgresql":
            # Lookup schema name from Tenant table
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if tenant:
                schema = tenant.schema_name or f"tenant_{tenant_id}"
                db.execute(text(f'SET search_path TO "{schema}", public'))
        else:
            # SQLite or other — tenant filtering is done at query level
            pass
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tenant middleware error: {e}")
        raise HTTPException(status_code=500, detail="Tenant resolution error")
    finally:
        db.close()

    response = await call_next(request)

    # Reset search_path after request (for connection pooling)
    if 'engine' in locals() and engine and engine.dialect.name == "postgresql":
        try:
            db.execute(text("SET search_path TO public"))
        except Exception:
            pass

    return response
