"""Tenant model for multi-tenant SaaS architecture.

Each tenant represents a separate company with its own schema, users, clients,
products, and invoices. This implements the schema-per-tenant pattern.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database import Base


class Tenant(Base):
    """Represents a company/tenant in the SaaS platform.

    Fields:
    - name: Company name
    - nit: Tax ID (Colombia) or equivalent
    - dian_resolution: DIAN resolution number
    - dian_resolution_date: Date of resolution
    - technical_key: Technical key provided by DIAN
    - certificate_path: Path to digital certificate (.p12)
    - certificate_password: Password for digital certificate (encrypted at rest)
    - is_active: Whether the tenant account is active
    - schema_name: PostgreSQL schema name for this tenant
    - created_at: Timestamp of creation
    """

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    nit = Column(String(20), unique=True, nullable=False, index=True)
    dian_resolution = Column(String(100), nullable=True)
    dian_resolution_date = Column(DateTime(timezone=True), nullable=True)
    technical_key = Column(String(255), nullable=True)
    certificate_path = Column(String(512), nullable=True)
    certificate_password = Column(Text, nullable=True)  # Encrypted
    is_active = Column(Boolean, default=True)
    schema_name = Column(String(63), unique=True, nullable=False)  # PG schema limit
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    users = relationship("User", back_populates="tenant")
    clients = relationship("Client", back_populates="tenant")
    products = relationship("Product", back_populates="tenant")
    invoices = relationship("InvoiceHeader", back_populates="tenant")

    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', nit='{self.nit}')>"
