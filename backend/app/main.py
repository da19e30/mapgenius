"""FastAPI application entry point.

- Registers CORS middleware (allow all origins for dev, tighten in prod).
- Includes authentication middleware.
- Mounts API routers.
- Exposes OpenAPI docs at /docs.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.middleware.auth_middleware import jwt_auth_middleware
from app.middleware.tenant_middleware import tenant_middleware
from app.routers import auth, invoices, tax, health
from app.routes import clients_router, products_router, invoice_management_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# CORS – restrict in production; allow localhost for dev
_ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# JWT auth middleware for protected routes
app.middleware("http")(jwt_auth_middleware)
app.middleware("http")(tenant_middleware)

# Register routers
app.include_router(auth.router)
app.include_router(invoices.router)
app.include_router(tax.router)
app.include_router(health.router)
app.include_router(clients_router)
app.include_router(products_router)
app.include_router(invoice_management_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

