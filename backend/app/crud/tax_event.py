"""CRUD utilities for TaxEvent model."""

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tax_event import TaxEvent, TaxStatus

async def create_tax_event(db: AsyncSession, invoice_id: int, country: str, xml_blob: bytes) -> TaxEvent:
    tax_event = TaxEvent(
        invoice_id=invoice_id,
        country=country,
        status=TaxStatus.pending,
        xml_blob=xml_blob,
    )
    db.add(tax_event)
    await db.commit()
    await db.refresh(tax_event)
    return tax_event

async def update_tax_status(db: AsyncSession, tax_event_id: int, status: TaxStatus, response_blob: bytes | None = None):
    stmt = (
        update(TaxEvent)
        .where(TaxEvent.id == tax_event_id)
        .values(status=status, response_blob=response_blob)
    )
    await db.execute(stmt)
    await db.commit()

async def get_tax_event(db: AsyncSession, tax_event_id: int) -> TaxEvent | None:
    result = await db.execute(select(TaxEvent).where(TaxEvent.id == tax_event_id))
    return result.scalars().first()
