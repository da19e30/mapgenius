"""Cliente de integración con la DIAN (Colombia).

Este cliente maneja:
- Generación de XML de factura electrónica según el esquema de la DIAN.
- Firma digital del XML usando una clave privada PEM (configurable vía variables de entorno).
- Envío del XML firmado al Web Service de la DIAN (simulado para pruebas).

En producción se conectaría al web service de la DIAN usando SOAP/REST con certificado digital.
Para el MVP emulamos el comportamiento:

1. Genera y firma el XML de la factura.
2. Decide si la factura es **aceptada** o **rechazada** (determinista basado en checksum).
3. Almacena un registro ``DianLog`` con el estado y detalle.
4. Retorna un diccionario ``{"status": "sent"|"error", "detail": str}``.

La clase es deliberadamente sin efectos secundarios aparte de la persistencia en BD,
facilitando el mocking en pruebas unitarias.
"""

import os
import random
import hashlib
from pathlib import Path
from typing import Dict
from lxml import etree

from app.models.dian_log import DianLog
from sqlalchemy.orm import Session
from app.database import SessionLocal


class DIANClient:
    """Cliente para interactuar con la DIAN (Colombia)."""

    def __init__(self):
        self.private_key_path = os.getenv("DIAN_PRIVATE_KEY", "backend/keys/dian_private_key.pem")
        self.certificate_path = os.getenv("DIAN_CERTIFICATE", "backend/keys/dian_certificate.pem")
        self.endpoint = os.getenv("DIAN_ENDPOINT", "https://vpfe.dian.gov.co/APIv2/invoice")

    def _build_xml(self, invoice_data: Dict) -> bytes:
        """Construye el XML de la factura según el esquema de la DIAN."""
        root = etree.Element("Invoice")
        for k, v in invoice_data.items():
            elem = etree.SubElement(root, k)
            elem.text = str(v)
        return etree.tostring(root, xml_declaration=True, encoding="utf-8")

    def _sign_xml(self, xml_bytes: bytes) -> bytes:
        """Firma el XML (simulado para el MVP)."""
        # En producción se usaría la clave privada y certificado
        root = etree.fromstring(xml_bytes)
        sig_elem = etree.SubElement(root, "Signature")
        sig_elem.text = hashlib.sha256(xml_bytes).hexdigest()
        cert_elem = etree.SubElement(root, "Certificate")
        cert_elem.text = "SIMULATED_CERTIFICATE"
        return etree.tostring(root, xml_declaration=True, encoding="utf-8")

    def generate_xml(self, invoice_data: Dict) -> bytes:
        """Genera el XML firmado de la factura."""
        xml = self._build_xml(invoice_data)
        return self._sign_xml(xml)

    def send(self, signed_xml: bytes) -> Dict:
        """Envía el XML firmado a la DIAN (simulado)."""
        return send_to_dian_simulation(signed_xml)

# Simple deterministic decision: if the SHA-256 of the file ends with an even digit → accepted
def _decision_from_file(file_path: str) -> str:
    try:
        import hashlib
        with open(file_path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        # Take last hex digit and decide
        last_digit = int(digest[-1], 16)
        return "accepted" if last_digit % 2 == 0 else "rejected"
    except Exception:
        # If any error occurs, treat as rejected to avoid false positives
        return "rejected"

def send_to_dian_simulation(signed_xml_path: str, db: Session = None) -> Dict[str, str]:
    """Simulate sending a signed invoice XML to DIAN.

    Parameters
    ----------
    signed_xml_path: str
        Absolute path to the signed XML file.

    Returns
    -------
    dict
        ``{"status": "accepted"|"rejected", "detail": "..."}``
    """
    if not os.path.isabs(signed_xml_path):
        raise ValueError("signed_xml_path must be an absolute path")
    if not Path(signed_xml_path).exists():
        raise FileNotFoundError(f"Signed XML not found: {signed_xml_path}")

    status = _decision_from_file(signed_xml_path)
    detail = (
        "Factura aceptada por DIAN (simulación)"
        if status == "accepted"
        else "Factura rechazada por DIAN (simulación) – verifique los datos"
    )

    # Persist log entry
    db = db if db is not None else SessionLocal()
    try:
        log = DianLog(
            invoice_cufe=Path(signed_xml_path).stem.replace("_signed", ""),
            request_xml_path=signed_xml_path,
            response_status=status,
            response_detail=detail,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

    return {"status": status, "detail": detail}
