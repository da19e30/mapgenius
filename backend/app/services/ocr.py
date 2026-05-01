"""
Servicio de OCR para procesar facturas y documentos financieros.

Este módulo:
- Recibe archivos PDF/JPG/PNG
- Extrae texto usando Tesseract OCR
- Valida idioma y calidad del texto extraído
- Devuelve texto procesado + metadatos
"""
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from app.models.invoice import Invoice
from app.services.file_validator import validate_file_extension, validate_file_size

# Configurar ruta de Tesseract (si no está en PATH)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Idiomas soportados
SUPPORTED_LANGUAGES = {"spa": "spa", "eng": "eng", "fra": "fra"}

def process_pdf_to_text(pdf_path: str, lang: str = "spa") -> str:
    """Convierte PDF a imágenes y extrae texto usando Tesseract."""
    pages = convert_from_path(pdf_path)
    full_text = ""
    for page in pages:
        text = pytesseract.image_to_string(page, lang=lang)
        full_text += text + "\n"
    return full_text

def process_image_to_text(image_path: str, lang: str = "spa") -> str:
    """Extrae texto de una imagen (JPG/PNG)."""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang=lang)

def process_file(file_path: str, file_type: str, lang: str = "spa") -> str:
    """Procesa cualquier archivo soportado y devuelve texto extraído."""
    if file_type == "pdf":
        return process_pdf_to_text(file_path, lang)
    elif file_type in ["jpg", "jpeg", "png"]:
        return process_image_to_text(file_path, lang)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {file_type}")

def extract_invoice_data(invoice: Invoice) -> dict:
    """Extrae datos estructurados de una factura usando OCR + NLP básico."""
    # Paso 1: Procesar archivo
    raw_text = process_file(invoice.filepath, invoice.file_type, invoice.ocr_language)

    # Paso 2: Validar calidad del texto
    if len(raw_text.strip()) < 50:
        invoice.ocr_status = "failed"
        invoice.save()
        raise ValueError("OCR falló: texto extraído insuficiente")

    # Paso 3: Guardar texto extraído
    invoice.extracted_text = raw_text
    invoice.ocr_status = "completed"
    invoice.processed_at = datetime.utcnow()
    invoice.save()

    # Paso 4: Parsear datos financieros (ejemplo básico)
    # En producción: usar NLP/ML para extraer totales, fechas, etc.
    return {
        "raw_text": raw_text,
        "word_count": len(raw_text.split()),
        "detected_language": invoice.ocr_language
    }
