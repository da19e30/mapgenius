"""Modelo para registrar cada interacción con la DIAN (simulada).

Almacena la petición XML, la respuesta simulada, timestamps y estado.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class DianLog(Base):
    __tablename__ = "dian_logs"

    id = Column(Integer, primary_key=True, index=True)
    invoice_cufe = Column(String(64), nullable=False, index=True)
    request_xml_path = Column(String(512), nullable=False)
    response_status = Column(String(20), nullable=False)  # accepted / rejected
    response_detail = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DianLog(id={self.id}, cufe={self.invoice_cufe}, status={self.response_status})>"
