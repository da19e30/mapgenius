import os
import sys

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Importar uvicorn y la app
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Iniciando servidor Mapgenius Solutions...")
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Presiona CTRL+C para detener.")
    uvicorn.run(app, host="0.0.0.0", port=8000)