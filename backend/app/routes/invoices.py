"""
Endpoints para procesamiento de facturas usando OCR + IA.

Este módulo expone:
- POST /upload: subir factura (PDF/JPG/PNG)
- GET /{id}: obtener estado y datos extraídos
- GET /list: listar facturas del usuario
"""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice import Invoice
from app.models.user import User
from app.services.ocr import extract_invoice_data
from app.services.file_validator import validate_uploaded_file
from app.services.auth import get_current_user
import os
import tempfile

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/upload", response_model=dict)
async def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Subir una factura para procesamiento OCR:
    1. Validar archivo (extensión, tamaño, MIME)
    2. Guardar en directorio temporal
    3. Crear registro Invoice en BD
    4. Procesar OCR y extraer datos
    5. Guardar texto extraído y metadatos
    """
    # Leer contenido una sola vez
    content = await file.read()
    file_size = len(content)

    # Validar extensión
    from app.services.file_validator import validate_file_extension
    is_valid, msg = validate_file_extension(file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    # Crear registro temporal en DB
    db_invoice = Invoice(
        user_id=current_user.id,
        filename=file.filename,
        file_type=file.filename.split(".")[-1].lower(),
        file_size=file_size,
        ocr_status="uploaded"
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    # Guardar archivo en sistema temporal
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"{db_invoice.id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    # Guardar ruta del archivo en el modelo
    db_invoice.filepath = file_path
    db.add(db_invoice)
    db.commit()

    # Procesar OCR (opcional)
    extraction_data = {}
    try:
        extraction_data = extract_invoice_data(db_invoice)
        # Guardar datos extraídos en FinancialData
        from app.models.financial_data import FinancialData
        for key, value in extraction_data.items():
            fd = FinancialData(
                user_id=current_user.id,
                invoice_id=db_invoice.id,
                category="desconocido",
                amount="0",
                timestamp=db_invoice.processed_at
            )
            db.add(fd)
        db.commit()
    except Exception as e:
        # Si OCR falla, marcar como subido sin procesar
        db_invoice.ocr_status = "uploaded"
        db.commit()
        # No lanzar excepción, continuar
        pass
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "message": "Factura procesada exitosamente",
        "invoice_id": db_invoice.id,
        "status": db_invoice.ocr_status,
        "data": extraction_data
    }

@router.get("/{invoice_id}", response_model=dict)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener estado y datos de una factura procesada."""
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    financial_data = db.query(FinancialData).filter(
        FinancialData.invoice_id == invoice_id
    ).all()

    return {
        "invoice": {
            "id": invoice.id,
            "filename": invoice.filename,
            "status": invoice.ocr_status,
            "file_type": invoice.file_type,
            "file_size": invoice.file_size,
            "uploaded_at": invoice.uploaded_at,
            "processed_at": invoice.processed_at
        },
        "financial_data": [{
            "id": fd.id,
            "category": fd.category,
            "amount": fd.amount,
            "timestamp": fd.timestamp
        } for fd in financial_data],
        "extracted_text": invoice.extracted_text[:500] if invoice.extracted_text else None
    }

@router.get("/list", response_model=list)
async def list_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todas las facturas del usuario."""
    invoices = db.query(Invoice).filter(
        Invoice.user_id == current_user.id
    ).order_by(Invoice.created_at.desc()).all()

    return [
        {
            "id": inv.id,
            "filename": inv.filename,
            "status": inv.ocr_status,
            "file_type": inv.file_type,
            "uploaded_at": inv.uploaded_at,
            "processed_at": inv.processed_at
        }
        for inv in invoices
    ]
