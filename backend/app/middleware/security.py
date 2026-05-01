"""Security middleware for FastAPI.

Features:
- Logging of suspicious requests (failed auth, large uploads, unexpected content‑type)
- Simple in‑memory IP blocklist for repeated failures (brute‑force mitigation)
- Validation of `Content‑Type` header on file‑upload endpoints
"""

import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# In‑memory store for failed attempts (IP -> [timestamp, …])
FAILED_ATTEMPTS = defaultdict(list)
BLOCKED_IPS = {}

# Configuration – adjust thresholds as needed
MAX_FAILURES = 5          # attempts
BLOCK_WINDOW = 300       # seconds (5 min) after which failures expire
BLOCK_DURATION = 900     # seconds (15 min) IP stays blocked


def _cleanup_attempts(ip: str, now: float) -> None:
    """Remove old timestamps older than BLOCK_WINDOW."""
    attempts = FAILED_ATTEMPTS[ip]
    FAILED_ATTEMPTS[ip] = [t for t in attempts if now - t < BLOCK_WINDOW]


def _is_blocked(ip: str, now: float) -> bool:
    if ip in BLOCKED_IPS:
        blocked_until = BLOCKED_IPS[ip]
        if now < blocked_until:
            return True
        else:
            # Unblock expired entry
            del BLOCKED_IPS[ip]
    return False


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Blocked IP handling
        if _is_blocked(client_ip, now):
            return JSONResponse({"detail": "IP blocked due to repeated failures"}, status_code=403)

        # Content‑Type validation for upload routes
        if request.url.path.startswith("/api/v1/invoices/upload"):
            ct = request.headers.get("content-type", "")
            # FastAPI's UploadFile uses multipart/form-data; reject anything else
            if "multipart/form-data" not in ct.lower():
                return JSONResponse({"detail": "Invalid Content-Type for file upload"}, status_code=400)

        response = await call_next(request)

        # Log suspicious activity – failed auth (401) or large uploads (>2 MB)
        if response.status_code == 401:
            # Record failure for brute‑force detection
            _cleanup_attempts(client_ip, now)
            FAILED_ATTEMPTS[client_ip].append(now)
            if len(FAILED_ATTEMPTS[client_ip]) >= MAX_FAILURES:
                BLOCKED_IPS[client_ip] = now + BLOCK_DURATION
        elif request.url.path.startswith("/api/v1/invoices/upload") and request.headers.get("content-length"):
            try:
                size = int(request.headers["content-length"])
                if size > 2 * 1024 * 1024:  # 2 MB – should have been caught by validator but double‑check
                    # Log oversized upload attempt
                    print(f"[SECURITY] Oversized upload from {client_ip}: {size} bytes")
            except ValueError:
                pass

        return response
