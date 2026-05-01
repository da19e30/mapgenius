"""CRUD utilities for the AuditLog model."""

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

async def log_action(
    db: AsyncSession,
    user_id: int | None,
    action: str,
    resource_type: str | None = None,
    resource_id: str | None = None,
    details: str | None = None,
) -> None:
    """Insert a row into the audit_log table.

    This helper does not return the inserted row; it simply commits.
    """
    stmt = insert(AuditLog).values(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
    )
    await db.execute(stmt)
    await db.commit()
