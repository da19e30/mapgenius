"""Rutas para la gestión completa de facturas electrónicas.

Incluye creación de facturas a partir de clientes y productos, generación de XML/Ubl, firma, envío a DIAN (simulado) y re‑envío por email.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.invoice_header import InvoiceHeader
from app.models.invoice_line import InvoiceLine
from app.models.client import Client
from app.models.product import Product
from app.models.user import User
from app.services.auth import get_current_user
from pydantic import BaseModel, validator

router = APIRouter(prefix="/invoices", tags=["invoices"])

class LineItem(BaseModel):
    product_id: int
    quantity: float
    unit_price: float | None = None  # opcional; si no se envía se usa price del producto
    iva_percent: float | None = None

    @validator("quantity")
    def qty_positive(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        return v

class InvoiceCreate(BaseModel):
    client_id: int
    line_items: List[LineItem]

    @validator("line_items")
    def at_least_one(cls, v):
        if not v:
            raise ValueError("Debe haber al menos una línea de detalle")
        return v

class InvoiceRead(BaseModel):
    id: int
    cufe: str
    status: str
    subtotal: float
    iva_total: float
    total_amount: float
    currency: str
    issue_date: str
    client: dict
    lines: List[dict]

    class Config:
        orm_mode = True

@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar cliente
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Preparar líneas y cálculos
    subtotal = 0.0
    iva_total = 0.0
    line_models = []
    for item in payload.line_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        unit_price = item.unit_price if item.unit_price is not None else product.price
        iva_percent = item.iva_percent if item.iva_percent is not None else product.iva_percent
        total_price = unit_price * item.quantity
        iva_amount = total_price * iva_percent / 100
        subtotal += total_price
        iva_total += iva_amount
        line = InvoiceLine(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=unit_price,
            total_price=total_price,
            iva_percent=iva_percent,
            iva_amount=iva_amount,
        )
        line_models.append(line)

    total_amount = subtotal + iva_total

    # Crear cabecera (CUFE y XML se generan después de guardar)
    header = InvoiceHeader(
        client_id=client.id,
        user_id=current_user.id,
        subtotal=subtotal,
        iva_total=iva_total,
        total_amount=total_amount,
        currency="COP",
        status="pending",
        cufe="",  # será rellenado por el servicio de generación
    )
    db.add(header)
    db.flush()  # obtener header.id sin commit

    # Asociar líneas
    for line in line_models:
        line.invoice_id = header.id
        db.add(line)

    db.commit()
    db.refresh(header)

    # Generar XML, firmar, calcular CUFE y guardar paths (lógica delegada a servicios)
    from app.services.invoice import generate_and_finalize_invoice
    generate_and_finalize_invoice(db, header.id)

    # Recargar para devolver información completa
    db.refresh(header)
    lines = db.query(InvoiceLine).filter(InvoiceLine.invoice_id == header.id).all()
    return InvoiceRead(
        id=header.id,
        cufe=header.cufe,
        status=header.status,
        subtotal=header.subtotal,
        iva_total=header.iva_total,
        total_amount=header.total_amount,
        currency=header.currency,
        issue_date=str(header.issue_date),
        client={"id": client.id, "nit": client.nit, "name": client.name},
        lines=[{
            "product_id": l.product_id,
            "quantity": l.quantity,
            "unit_price": l.unit_price,
            "total_price": l.total_price,
            "iva_percent": l.iva_percent,
            "iva_amount": l.iva_amount,
        } for l in lines],
    )

@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    header = db.query(InvoiceHeader).filter(InvoiceHeader.id == invoice_id, InvoiceHeader.user_id == current_user.id).first()
    if not header:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    client = db.query(Client).filter(Client.id == header.client_id).first()
    lines = db.query(InvoiceLine).filter(InvoiceLine.invoice_id == header.id).all()
    return InvoiceRead(
        id=header.id,
        cufe=header.cufe,
        status=header.status,
        subtotal=header.subtotal,
        iva_total=header.iva_total,
        total_amount=header.total_amount,
        currency=header.currency,
        issue_date=str(header.issue_date),
        client={"id": client.id, "nit": client.nit, "name": client.name},
        lines=[{
            "product_id": l.product_id,
            "quantity": l.quantity,
            "unit_price": l.unit_price,
            "total_price": l.total_price,
            "iva_percent": l.iva_percent,
            "iva_amount": l.iva_amount,
        } for l in lines],
    )
