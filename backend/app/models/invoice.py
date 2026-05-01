"""Invoice ORM model.

Fields include status workflow, monetary fields, XML/PDF storage (as binary blobs), and timestamps.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    validated = "validated"
    sent = "sent"
    rejected = "rejected"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    external_id = Column(String, unique=True, nullable=True)  # e.g., DIAN/SAT identifier
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft, nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    due_at = Column(DateTime(timezone=True), nullable=True)
    xml_blob = Column(LargeBinary, nullable=True)   # generated XML document
    pdf_blob = Column(LargeBinary, nullable=True)   # PDF representation for user download
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="invoices")
    tax_events = relationship("TaxEvent", back_populates="invoice")