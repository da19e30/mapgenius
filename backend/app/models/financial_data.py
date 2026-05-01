"""
Modelo de datos financieros extraídos de facturas mediante OCR + IA.

Este módulo define la tabla 'financial_data' para almacenar:
- Categorías de gastos/ingresos (automáticamente clasificadas por IA)
- Montos extraídos
- Timestamps de transacción
- Relaciones con facturas y usuarios
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # ej: "alimentación", "transporte", "servicios"
    amount = Column(String(50), nullable=False)     # almacenado como string para precisión decimal
    currency = Column(String(3), default="USD")     # moneda (USD, EUR, etc.)
    transaction_date = Column(DateTime)             # fecha de la transacción en la factura
    rfc_emisor = Column(String(100))                # RFC del emisor extraído por IA
    rfc_receptor = Column(String(100))              # RFC del receptor
    invoice_number = Column(String(100))            # folio de la factura
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(String(10))           # score de confianza de la IA (0-1)

    # Relaciones
    user = relationship("User", back_populates="financial_data")
    invoice = relationship("Invoice", back_populates="financial_data")

    def __repr__(self):
        return f"<FinancialData(id={self.id}, category='{self.category}', amount='{self.amount}')>"