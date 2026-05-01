from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.financial_data import FinancialData
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/financial-data", tags=["financial-data"])

@router.get("/list", response_model=list)
async def list_financial_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todos los registros financieros del usuario autenticado."""
    records = (
        db.query(FinancialData)
        .filter(FinancialData.user_id == current_user.id)
        .order_by(FinancialData.extracted_at.desc())
        .all()
    )
    if not records:
        return []
    return [
        {
            "id": r.id,
            "category": r.category,
            "amount": r.amount,
            "currency": r.currency,
            "transaction_date": r.transaction_date,
            "rfc_emisor": r.rfc_emisor,
            "invoice_id": r.invoice_id,
            "created_at": r.extracted_at,
        }
        for r in records
    ]
