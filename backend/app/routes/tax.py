"""Rutas para exportación fiscal (DIAN y SAT)."""

from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import Literal

from app.database import get_db
from app.models.invoice import Invoice
from app.models.tax_export_log import TaxExportLog, TaxCountry, ExportStatus
from app.services.auth import get_current_user
from app.services.dian_client import DIANClient
from app.services.sat_client import SATClient

router = APIRouter(prefix="/tax", tags=["tax"])

def _load_invoice(db: Session, invoice_id: int, user_id: int) -> Invoice:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return invoice

@router.post("/export/{country}")
async def export_invoice(
    country: Literal["CO", "MX"],
    invoice_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Exporta una factura a la autoridad fiscal correspondiente.

    - **country**: "CO" para DIAN, "MX" para SAT.
    - **invoice_id**: ID de la factura a exportar (propietario = usuario autenticado).
    """
    invoice = _load_invoice(db, invoice_id, current_user.id)
    # Preparar datos mínimos para XML
    invoice_data = {
        "invoice_number": invoice.invoice_number,
        "issue_date": invoice.issue_date,
        "total_amount": invoice.total_amount,
        "currency": invoice.currency,
        "rfc_emisor": invoice.rfc_emisor,
        "rfc_receptor": invoice.rfc_receptor,
    }
    if country == "CO":
        client = DIANClient()
    else:
        client = SATClient()
    # Generar XML firmado
    signed_xml = client.generate_xml(invoice_data)
    # Enviar a la autoridad (simulado)
    response = client.send(signed_xml)
    # Persistir log
    log = TaxExportLog(
        tenant_id=current_user.id,
        invoice_id=invoice.id,
        country=TaxCountry(country),
        xml_content=signed_xml.decode(),
        status=ExportStatus.SENT if response["status"] == "sent" else ExportStatus.ERROR,
        response_message=response["detail"],
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"export_id": log.id, "status": log.status.value, "detail": response["detail"]}
