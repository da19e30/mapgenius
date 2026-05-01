"""Invoice CRUD routes (protected)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db.session import get_db

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])

@router.post("/", response_model=schemas.invoice.InvoiceRead)
async def create_invoice(request: Request, payload: schemas.invoice.InvoiceCreate, db: AsyncSession = Depends(get_db)):
    owner_id = getattr(request.state, "user_id", None)
    if owner_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    invoice = await crud.invoice.create_invoice(
        db,
        owner_id=int(owner_id),
        total_amount=payload.total_amount,
        currency=payload.currency,
        due_at=payload.due_at,
        external_id=payload.external_id,
    )
    return invoice

@router.get("/{invoice_id}", response_model=schemas.invoice.InvoiceRead)
async def read_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = await crud.invoice.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice
