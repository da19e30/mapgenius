"""
Script mínimo para iniciar Mapgenius Backend.
Evita importar módulos problemáticos (spacy, etc.) para una carga rápida.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Importar solo lo esencial
from app.database import init_db
init_db()  # Crea tablas si no existen

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Iniciando servidor Mapgenius Solutions...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Presiona CTRL+C para detener.\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)