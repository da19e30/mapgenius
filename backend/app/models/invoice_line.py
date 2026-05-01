'''Modelo de línea de factura electrónica.

Cada registro representa un ítem (producto/servicio) incluido en una factura.
'''

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class InvoiceLine(Base):
    """Representa una línea de detalle dentro de una factura.

    Campos:
    - invoice_id: FK a la cabecera de la factura
    - product_id: FK al producto/servicio
    - quantity: Cantidad del ítem
    - unit_price: Precio unitario sin IVA
    - total_price: Precio total (unit_price * quantity)
    - iva_percent: Porcentaje de IVA aplicado a esta línea
    - iva_amount: Monto de IVA calculado
    """

    __tablename__ = "invoice_lines"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoice_headers.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    iva_percent = Column(Float, default=19.0)
    iva_amount = Column(Float, nullable=False)

    # Relaciones
    invoice = relationship("InvoiceHeader", back_populates="lines")
    product = relationship("Product", back_populates="line_items")

    def __repr__(self):
        return f"<InvoiceLine(id={self.id}, product_id={self.product_id}, qty={self.quantity})>"
