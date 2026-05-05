"""User ORM model.

Fields:
- email (unique, indexed)
- hashed_password
- full_name (optional)
- role (enum: admin, accountant, viewer)
- is_active (bool)
- created_at (timestamp)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from .invoice_header import InvoiceHeader
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    accountant = "accountant"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.accountant, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    invoices = relationship("InvoiceHeader", back_populates="user")
    invoice_records = relationship("Invoice", back_populates="owner")
    financial_data = relationship("FinancialData", back_populates="user")