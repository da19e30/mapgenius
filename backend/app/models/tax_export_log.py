'''Modelo para registrar exportaciones de facturas a autoridades fiscales (DIAN, SAT).'''

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TaxCountry(str, enum.Enum):
    CO = "CO"
    MX = "MX"

class ExportStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    ERROR = "error"

class TaxExportLog(Base):
    __tablename__ = "tax_export_log"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, index=True)  # assuming tenant_id is stored on invoice
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    country = Column(Enum(TaxCountry), nullable=False)
    xml_content = Column(Text, nullable=False)
    status = Column(Enum(ExportStatus), nullable=False, default=ExportStatus.PENDING)
    response_message = Column(Text)  # raw response from authority
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="tax_exports")

    def __repr__(self):
        return f"<TaxExportLog(id={self.id}, country={self.country}, status={self.status})>"
