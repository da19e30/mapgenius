"""Cliente de integración con la DIAN (Colombia).

Este cliente maneja:
- Generación de XML de factura electrónica según el esquema de la DIAN.
- Firma digital del XML usando una clave privada PEM (configurable vía variables de entorno).
- Envío del XML firmado al Web Service de la DIAN (simulado para pruebas).
"""

In a production system this would call the real DIAN web‑service using SOAP/REST with a
digital certificate. For the MVP we emulate the behaviour:

1. Read the signed XML file supplied by ``send_to_dian_simulation``.
2. Randomly decide whether the invoice is **accepted** or **rejected** (deterministic
   based on a simple checksum so tests can be reproducible).
3. Store a ``DianLog`` record with the request path, status and optional detail.
4. Return a dictionary ``{"status": <"accepted"|"rejected">, "detail": str}``.

The function is deliberately side‑effect‑free apart from DB persistence, making it
easy to mock in unit tests.
"""

import os
import random
from pathlib import Path
from typing import Dict

from app.models.dian_log import DianLog
from app.database import SessionLocal

# Simple deterministic decision: if the SHA‑256 of the file ends with an even digit → accepted
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

def send_to_dian_simulation(signed_xml_path: str) -> Dict[str, str]:
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
    db = SessionLocal()
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
