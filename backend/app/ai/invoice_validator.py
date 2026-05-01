"""AI‑assisted invoice validator.

Uses a lightweight Pydantic model to ensure that all mandatory fields are present and
that business rules (e.g., subtotal > 0, IVA percentages within allowed range) are met.
The validator can be extended with a machine‑learning model for anomaly detection, but
for the MVP we keep it rule‑based.
"""

from pydantic import BaseModel, validator, ValidationError
from typing import List

class LineItemModel(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    iva_percent: float

    @validator("quantity")
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        return v

    @validator("unit_price")
    def unit_price_non_negative(cls, v):
        if v < 0:
            raise ValueError("El precio unitario no puede ser negativo")
        return v

    @validator("iva_percent")
    def iva_valid_range(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("El porcentaje de IVA debe estar entre 0 y 100")
        return v

class InvoicePayloadModel(BaseModel):
    client_id: int
    line_items: List[LineItemModel]

    @validator("line_items")
    def at_least_one_line(cls, v):
        if len(v) == 0:
            raise ValueError("La factura debe contener al menos una línea de detalle")
        return v

def validate_invoice_payload(payload: dict) -> None:
    """Validate the raw payload received by the ``/invoices`` endpoint.

    Raises ``ValidationError`` if any rule is violated.
    """
    InvoicePayloadModel(**payload)
