"""Pydantic schemas for Invoice API."""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum

class InvoiceStatus(str, Enum):
    draft = "draft"
    validated = "validated"
    sent = "sent"
    rejected = "rejected"

class InvoiceBase(BaseModel):
    total_amount: float
    currency: str = Field(default="USD", max_length=3)
    due_at: datetime | None = None

class InvoiceCreate(InvoiceBase):
    external_id: str | None = None

class InvoiceRead(InvoiceBase):
    id: int
    owner_id: int
    status: InvoiceStatus
    issued_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
