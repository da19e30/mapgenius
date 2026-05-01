"""Reporting endpoints for the dashboard.

Provides a simple summary required by the frontend dashboard:
- total_income: sum of total_amount of accepted invoices
- pending_count: number of invoices with status 'pending'
- accepted_count: number of invoices with status 'accepted'
- rejected_count: number of invoices with status 'rejected'
- total_iva: sum of iva_total of accepted invoices
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.invoice_header import InvoiceHeader

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    # Total income (only accepted invoices)
    total_income = db.query(func.coalesce(func.sum(InvoiceHeader.total_amount), 0)).filter(InvoiceHeader.status == "accepted").scalar()
    total_iva = db.query(func.coalesce(func.sum(InvoiceHeader.iva_total), 0)).filter(InvoiceHeader.status == "accepted").scalar()
    # Status counts
    counts = db.query(InvoiceHeader.status, func.count()).group_by(InvoiceHeader.status).all()
    status_map = {status: cnt for status, cnt in counts}
    return {
        "total_income": float(total_income),
        "total_iva": float(total_iva),
        "pending_count": status_map.get("pending", 0),
        "accepted_count": status_map.get("accepted", 0),
        "rejected_count": status_map.get("rejected", 0),
    }
