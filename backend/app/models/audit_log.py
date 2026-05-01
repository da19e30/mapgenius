"""Model for audit logging of critical actions."""

from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Null for system actions
    action = Column(String, nullable=False)   # e.g., "login", "create_invoice"
    resource_type = Column(String, nullable=True)  # e.g., "invoice"
    resource_id = Column(String, nullable=True)   # ID of the resource
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String, nullable=True)  # optional JSON string with extra info
