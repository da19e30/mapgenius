from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.auth import get_current_user
from app.models.user import User
from app.ai.ocr_enhancer import get_enhancer

router = APIRouter(prefix="/ocr", tags=["ocr"])

class OCRRequest(BaseModel):
    text: str

@router.post("/enhance")
async def enhance_ocr(request: OCRRequest, current_user: User = Depends(get_current_user)):
    """Recibe texto OCR y devuelve los campos estructurados detectados.

    - No persiste nada en la base de datos, solo procesa y devuelve.
    - Usa el motor OCREnhancer que protege la importación de spaCy.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto OCR no puede estar vacío")
    enhancer = get_enhancer()
    result = enhancer.enhance(request.text)
    return result
