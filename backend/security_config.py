"""Security configuration for FastAPI application.

Provides:
- Rate limiting settings (using slowapi)
- Secure HTTP headers (HSTS, CSP, X‑Frame‑Options, Referrer‑Policy)
- Input validation helpers
- File upload sanitisation utilities
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
# Limit auth endpoints to 5 requests per minute per IP to mitigate brute‑force
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Example per‑endpoint limit (to be applied in router definitions)
auth_rate_limit = "5/minute"

# ---------------------------------------------------------------------------
# Security headers middleware
# ---------------------------------------------------------------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security‑related HTTP headers to every response.

    * HSTS – force HTTPS (max‑age 1 year, include subdomains)
    * CSP – restrict sources to own origin and allow images from data URLs
    * X‑Frame‑Options – clickjacking protection
    * Referrer‑Policy – limit referrer information
    * X‑Content-Type‑Options – prevent MIME sniffing
    """
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        # HSTS (only sent over HTTPS – FastAPI should be behind TLS termination)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        # Content Security Policy – adjust as needed for frontend assets
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none';"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

# ---------------------------------------------------------------------------
# Input validation helpers (can be imported in routes/services)
# ---------------------------------------------------------------------------
def is_valid_email(email: str) -> bool:
    import re
    # Simple RFC‑5322‑compatible regex
    pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@" \
              r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?" \
              r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    return re.fullmatch(pattern, email) is not None

# ---------------------------------------------------------------------------
# File upload sanitisation (wrapper around existing validator)
# ---------------------------------------------------------------------------
def sanitize_filename(filename: str) -> str:
    """Return a safe filename – remove path traversal and unsafe chars."""
    import os, re
    # Remove directory components
    name = os.path.basename(filename)
    # Allow only alphanumerics, dash, underscore, dot
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name
