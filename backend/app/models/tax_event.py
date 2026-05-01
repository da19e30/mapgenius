"""Model for storing tax authority communication events (XML sent, response, etc.)."""

from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TaxStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"

class TaxEvent(Base):
    __tablename__ = "tax_events"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    country = Column(String(2), nullable=False)  # CO, MX, etc.
    status = Column(Enum(TaxStatus), default=TaxStatus.pending, nullable=False)
    xml_blob = Column(LargeBinary, nullable=True)
    response_blob = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="tax_events")
