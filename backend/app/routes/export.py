from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice
from app.models.financial_data import FinancialData
from app.services.auth import get_current_user
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/invoices")
async def export_invoices(db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """Exporta las facturas del usuario en formato CSV."""
    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).all()
    if not invoices:
        raise HTTPException(status_code=404, detail="No hay facturas para exportar")
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'filename', 'total_amount', 'currency', 'uploaded_at', 'status', 'invoice_number', 'rfc_emisor'])
    for inv in invoices:
        writer.writerow([
            inv.id,
            inv.filename,
            inv.total_amount,
            inv.currency,
            inv.uploaded_at,
            inv.ocr_status,
            inv.invoice_number,
            inv.rfc_emisor
        ])
    output.seek(0)
    return StreamingResponse(
        output,
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename=invoices_{current_user.id}.csv'}
    )

@router.get("/financial-data")
async def export_financial_data(db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    """Exporta los datos financieros del usuario en formato CSV."""
    records = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No hay datos financieros para exportar")
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'category', 'amount', 'currency', 'transaction_date', 'rfc_emisor', 'invoice_number', 'extracted_at'])
    for r in records:
        writer.writerow([
            r.id,
            r.category,
            r.amount,
            r.currency,
            r.transaction_date,
            r.rfc_emisor,
            r.invoice_number,
            r.extracted_at
        ])
    output.seek(0)
    return StreamingResponse(
        output,
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename=financial_data_{current_user.id}.csv'}
    )
