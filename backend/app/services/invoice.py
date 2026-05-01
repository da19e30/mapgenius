"""Service layer for electronic invoice lifecycle.

- generate_xml: builds UBL XML using utils.xml_utils
- sign_xml: adds RSA signature via utils.signature
- compute_cufe: SHA‑256 hash (already in xml_utils)
- generate_qr: simple base64 encoding of CUFE (placeholder for real QR spec)
- send_to_dian: calls the simulated DIAN client service
- finalize_invoice: orchestrates the whole flow and persists paths/status

Now integrates AI validation (invoice_validator) and PDF generation (pdf_generator).
"""

import os
from datetime import datetime
from typing import List, Dict

from app.models.invoice_header import InvoiceHeader
from app.models.invoice_line import InvoiceLine
from app.models.client import Client
from app.models.product import Product
from app.utils.xml_utils import generate_invoice_xml, compute_cufe
from app.utils.signature import sign_xml
from app.services.dian_client import send_to_dian_simulation
from app.services.email import send_invoice_email
from app.services.pdf_generator import render_invoice_pdf
from app.ai.invoice_validator import validate_invoice_payload
from app.database import SessionLocal

# Directory where generated artefacts are stored (XML, signed XML, PDF, QR)
BASE_OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated"))

def _ensure_output_dir():
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

def _collect_header_data(header: InvoiceHeader, client: Client) -> Dict:
    return {
        "cufe": header.cufe or "",
        "issue_date": header.issue_date.isoformat(),
        "currency": header.currency,
        "emisor_nit": os.getenv("EMISOR_NIT", "900123456"),
        "emisor_name": os.getenv("EMISOR_NAME", "Mapgenius Solutions Ltd"),
        "client": {
            "nit": client.nit,
            "name": client.name,
            "address": client.address or "",
        },
        "subtotal": header.subtotal,
        "total": header.total_amount,
    }

def _collect_line_data(lines: List[InvoiceLine]) -> List[Dict]:
    result = []
    for line in lines:
        # Ensure product relationship is loaded
        if not hasattr(line, "product"):
            db = SessionLocal()
            line.product = db.query(Product).filter(Product.id == line.product_id).first()
            db.close()
        result.append({
            "product_code": line.product.code if line.product else "",
            "product_name": line.product.name if line.product else "",
            "description": line.product.name if line.product else "",
            "quantity": line.quantity,
            "unit_price": line.unit_price,
            "total_price": line.total_price,
            "iva_percent": line.iva_percent,
            "iva_amount": line.iva_amount,
        })
    return result

def generate_and_finalize_invoice(db_session, header_id: int, raw_payload: dict = None):
    """Full pipeline for a freshly created InvoiceHeader.

    Parameters
    ----------
    db_session: Session
        Active SQLAlchemy session.
    header_id: int
        Identifier of the InvoiceHeader just persisted.
    raw_payload: dict, optional
        Original payload received by the API (used for AI validation). If provided,
        ``invoice_validator.validate_invoice_payload`` is executed before proceeding.
    """
    _ensure_output_dir()
    header: InvoiceHeader = db_session.query(InvoiceHeader).filter(InvoiceHeader.id == header_id).first()
    if not header:
        raise ValueError(f"InvoiceHeader {header_id} not found")
    client: Client = db_session.query(Client).filter(Client.id == header.client_id).first()
    lines: List[InvoiceLine] = db_session.query(InvoiceLine).filter(InvoiceLine.invoice_id == header.id).all()

    # ---- AI validation (if payload supplied) ----
    if raw_payload is not None:
        try:
            validate_invoice_payload(raw_payload)
        except Exception as e:
            header.status = "rejected"
            db_session.add(header)
            db_session.commit()
            raise ValueError(f"Invoice validation failed: {e}")

    # ---- XML generation ----
    header_data = _collect_header_data(header, client)
    line_data = _collect_line_data(lines)
    xml_str = generate_invoice_xml(header_data, line_data)
    # ---- CUFE computation ----
    cufe = compute_cufe(xml_str)
    header.cufe = cufe
    # ---- Signature ----
    signed_xml = sign_xml(xml_str)
    # ---- Persist XML files ----
    xml_path = os.path.join(BASE_OUTPUT_DIR, f"{cufe}.xml")
    signed_path = os.path.join(BASE_OUTPUT_DIR, f"{cufe}_signed.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    with open(signed_path, "w", encoding="utf-8") as f:
        f.write(signed_xml)
    header.xml_path = xml_path
    db_session.add(header)
    db_session.commit()

    # ---- Simulate DIAN submission ----
    dian_response = send_to_dian_simulation(signed_path)
    header.status = dian_response["status"]
    db_session.add(header)
    db_session.commit()

    # ---- PDF generation & email (if accepted) ----
    if header.status == "accepted":
        pdf_path = os.path.join(BASE_OUTPUT_DIR, f"{cufe}.pdf")
        pdf_data = {
            "emisor_name": header_data["emisor_name"],
            "emisor_nit": header_data["emisor_nit"],
            "client": header_data["client"],
            "issue_date": header_data["issue_date"],
            "cufe": cufe,
            "lines": line_data,
            "subtotal": header.subtotal,
            "iva_total": header.iva_total,
            "total_amount": header.total_amount,
            "currency": header.currency,
        }
        render_invoice_pdf(pdf_data, pdf_path)
        header.pdf_path = pdf_path
        db_session.add(header)
        db_session.commit()
        # ---- Send email to client ----
        if client.email:
            send_invoice_email(to=client.email, xml_path=signed_path, pdf_path=pdf_path)
    return header
