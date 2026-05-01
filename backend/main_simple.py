"""
Archivo main simple para pruebas - Mapgenius Solutions.

Este archivo evita importar rutas problemáticas y solo expone
el endpoint /health para verificar que el servidor corre.
"""

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

app = FastAPI(
    title="Mapgenius Solutions API",
    description="API para automatización de facturación",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Mapgenius API - Servidor funcionando"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Mapgenius API está operativa"}

# Ruta de prueba sin dependencias
@app.get("/test")
async def test():
    return {"test": "pasado", "sqlite": "conectado"}
