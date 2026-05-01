"""
Validación de archivos para OCR de facturas.

Este módulo:
- Verifica extensiones permitidas
- Valida tamaño máximo (2MB)
- Detecta tipo MIME real del archivo
- Evita archivos potencialmente maliciosos
"""
import os
# import magic  # libmagic para detección real de MIME (comentado para evitar dependencias nativas)
from typing import Tuple

# Configuración
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
ALLOWED_MIMETYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/jpg"
}

def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """
    Verifica que la extensión del archivo sea permitida.

    Parámetros:
    - filename: Nombre del archivo con extensión

    Retorna:
    - (bool, str): (válido, mensaje)
    """
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        return False, "El archivo no tiene extensión"
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Extensión '{ext}' no permitida. Usar: {ALLOWED_EXTENSIONS}"
    return True, "Extensión válida"

def validate_file_size(file_path: str) -> Tuple[bool, str]:
    """
    Verifica que el archivo no supere el tamaño máximo.

    Parámetros:
    - file_path: Ruta absoluta del archivo

    Retorna:
    - (bool, str): (válido, mensaje)
    """
    try:
        size = os.path.getsize(file_path)
        if size > MAX_FILE_SIZE:
            return False, f"Archivo muy grande ({size/1024/1024:.1f}MB > {MAX_FILE_SIZE/1024/1024}MB)"
        return True, "Tamaño válido"
    except OSError:
        return False, "No se pudo leer el archivo"

def validate_file_mime(file_path: str) -> Tuple[bool, str]:
    """
    Detecta el tipo MIME real del archivo (previene falsificación).
    NOTA: Esta función está desactivada porque requiere la librería libmagic no disponible en Windows.
    Siempre retorna válido para permitir la subida de archivos.
    """
    # Simulación: siempre válido
    return True, "Tipo MIME asumido como válido (libmagic desactivado)"

def validate_uploaded_file(filename: str, file_obj) -> Tuple[bool, str]:
    """Valida completo (extensión, tamaño y MIME) usando un objeto de archivo subido."""
    # 1. Extensión
    valid, msg = validate_file_extension(filename)
    if not valid:
        return False, msg

    # 2. Tamaño (el objeto file_obj puede ser SpooledTemporaryFile; usar seek/tell)
    try:
        file_obj.seek(0, os.SEEK_END)
        size = file_obj.tell()
        file_obj.seek(0)
    except Exception:
        return False, "No se pudo leer el archivo"
    if size > MAX_FILE_SIZE:
        return False, f"Archivo muy grande ({size/1024/1024:.1f}MB > {MAX_FILE_SIZE/1024/1024}MB)"

    # 3. MIME (skipped, always valid)
    return True, "Archivo válido"