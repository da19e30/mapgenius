'''Modelo de producto/servicio para la facturación electrónica.

Define la tabla `products` con la información requerida por la DIAN para la clasificación de ítems.
'''

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    """Representa un producto o servicio que puede incluirse en una factura.

    Campos:
    - code: Código interno o SKU del producto (único)
    - name: Nombre descriptivo
    - price: Precio unitario sin IVA
    - iva_percent: Porcentaje de IVA aplicable (ej. 19.0)
    - dian_class: Código de clasificación DIAN (opcional)
    - unit: Unidad de medida (ej. "unidad", "kg", "hora")
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    iva_percent = Column(Float, default=19.0)  # IVA estándar en Colombia
    dian_class = Column(String(20), nullable=True)
    unit = Column(String(20), nullable=False, default="unidad")

    # Relaciones
    line_items = relationship("InvoiceLine", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, code='{self.code}', name='{self.name}')>"
