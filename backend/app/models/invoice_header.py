'''Modelo de cabecera de factura electrónica.

Separa la información de la factura en una tabla de cabecera y una de líneas para cumplir con la normativa DIAN.
'''

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class InvoiceHeader(Base):
    """Representa la cabecera de una factura electrónica.

    Campos principales:
    - client_id: FK al cliente receptor
    - user_id: FK al usuario que crea la factura
    - issue_date: Fecha de emisión
    - total_amount: Total de la factura (incluye IVA)
    - subtotal: Subtotal sin IVA
    - iva_total: Total IVA aplicado
    - currency: Moneda (ej. COP)
    - cufe: Código Único de Factura Electrónica (generado)
    - status: Estado del proceso DIAN (pending, accepted, rejected)
    """

    __tablename__ = "invoice_headers"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    subtotal = Column(Float, nullable=False)
    iva_total = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="COP")
    cufe = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    xml_path = Column(String(512), nullable=True)
    pdf_path = Column(String(512), nullable=True)

    # Relaciones
    client = relationship("Client", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InvoiceHeader(id={self.id}, cufe='{self.cufe}', status='{self.status}')>"
