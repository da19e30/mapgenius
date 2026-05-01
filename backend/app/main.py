"""FastAPI application entry point.

- Registers CORS middleware (allow all origins for dev, tighten in prod).
- Includes authentication middleware.
- Mounts API routers.
- Exposes OpenAPI docs at /docs.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.auth_middleware import jwt_auth_middleware
from app.routers import auth, invoices, tax, health

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# CORS – allow all origins in development; adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT auth middleware for protected routes
app.middleware("http")(jwt_auth_middleware)

# Register routers
app.include_router(auth.router)
app.include_router(invoices.router)
app.include_router(tax.router)
app.include_router(health.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

