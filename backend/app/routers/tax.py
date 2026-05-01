"""Router for tax‑authority XML generation and sending.

Endpoints (prototipo):
- POST /{invoice_id}/generate   → crea XML y registra TaxEvent con estado pending
- POST /{tax_event_id}/send     → envía XML al ente (DIAN/SAT) y actualiza el estado
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app import crud
from app.services import tax as tax_service
from app.models.tax_event import TaxStatus

# New imports for audit logging and XSD validation
from app.crud.audit_log import log_action
from app.services.tax import validate_xml

router = APIRouter(prefix="/api/v1/tax", tags=["tax"])

@router.post("/{invoice_id}/generate", response_model=dict)
async def generate_xml(
    invoice_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Genera el XML de una factura y crea un TaxEvent en estado *pending*.
    Sólo el propietario de la factura puede ejecutar esta acción.
    """
    owner_id = getattr(request.state, "user_id", None)
    invoice = await crud.invoice.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    if owner_id is None or int(owner_id) != invoice.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Construir payload mínimo para el XML (adaptar campos reales según requerimientos)
    payload = {
        "id": invoice.id,
        "issued_at": invoice.issued_at,
        "total_amount": invoice.total_amount,
        "currency": invoice.currency,
        "issuer": "YOUR_COMPANY",  # TODO: cargar de configuración / empresa
        "receiver": "CLIENT",      # TODO: obtener del cliente asociado
    }
    xml_blob = tax_service.generate_xml(payload)

    # Por ahora fijamos el país a CO (Colombia). En producción será dinámico.
    tax_event = await crud.tax_event.create_tax_event(
        db,
        invoice_id=invoice.id,
        country="CO",
        xml_blob=xml_blob,
    )
    # Audit log for tax XML generation
    await log_action(db, action="tax_xml_generated", tax_event_id=tax_event.id, user_id=owner_id)
    return {"tax_event_id": tax_event.id, "status": tax_event.status.value}

@router.post("/{tax_event_id}/send", response_model=dict)
async def send_xml(
    tax_event_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Envía el XML previamente generado a la autoridad fiscal.
    Actualiza el estado del TaxEvent según la respuesta simulada.
    """
    owner_id = getattr(request.state, "user_id", None)
    tax_event = await crud.tax_event.get_tax_event(db, tax_event_id)
    if not tax_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax event not found")
    # Verificar que el usuario sea propietario de la factura asociada
    if owner_id is None or int(owner_id) != tax_event.invoice.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if not tax_event.xml_blob:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="XML not generated")

    # Validate XML against XSD before sending
    try:
        validate_xml(tax_event.xml_blob)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"XML validation error: {e}")

    # Simular envío al ente fiscal (DIAN/SAT)
    result = tax_service.send_to_authority(tax_event.xml_blob, tax_event.country)
    new_status = TaxStatus.sent if result["status"] == "sent" else TaxStatus.rejected
    await crud.tax_event.update_tax_status(
        db,
        tax_event_id=tax_event.id,
        status=new_status,
        response_blob=result.get("detail", "").encode(),
    )
    # Audit log for tax XML send attempt
    await log_action(db, action="tax_xml_sent", tax_event_id=tax_event.id, user_id=owner_id, status=new_status.value)
    return {"tax_event_id": tax_event.id, "new_status": new_status.value, "detail": result.get("detail")}
