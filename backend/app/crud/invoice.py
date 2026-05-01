"""CRUD utilities for Invoice model."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.invoice import Invoice

async def create_invoice(db: AsyncSession, owner_id: int, total_amount: float, currency: str = "USD", due_at=None, external_id: str | None = None) -> Invoice:
    invoice = Invoice(
        owner_id=owner_id,
        total_amount=total_amount,
        currency=currency,
        due_at=due_at,
        external_id=external_id,
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice

async def get_invoice(db: AsyncSession, invoice_id: int) -> Invoice | None:
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    return result.scalars().first()
