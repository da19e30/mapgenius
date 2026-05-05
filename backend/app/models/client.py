'''Modelo de cliente para la facturación electrónica.

Este módulo define la tabla `clients` que almacena información fiscal de los clientes según la normativa colombiana.
'''

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    """Representa un cliente o ente receptor de facturas.

    Campos obligatorios según DIAN:
    - nit: Número de Identificación Tributaria (único)
    - name: Razón social o nombre completo
    - email: Correo electrónico de contacto
    - address: Dirección fiscal
    - tax_regime: Régimen tributario del cliente
    """

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True, index=True)
    nit = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    tax_regime = Column(String(100), nullable=False)

    # Relaciones
    tenant = relationship("Tenant", back_populates="clients")
    invoices = relationship("InvoiceHeader", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, nit='{self.nit}', name='{self.name}')>"
