"""
Package init for routes.
Import and expose routers for use in main.py.
"""
from .user import router as user_router
from .invoices import router as invoices_router
from .financial import router as financial_router
# AI routes commented out temporarily to avoid spacy dependency
from .tax import router as tax_router
# from .ai_routes import router as ai_router

__all__ = ["user_router", "invoices_router", "financial_router", "tax_router"]  # "ai_router" commented out
