"""HTTP middleware that validates JWT for protected routes.

Public routes (registration, login, token refresh) are excluded.
The user ID extracted from the token is stored in ``request.state.user_id``.
"""

from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.security import decode_token
from app.core.config import settings

PUBLIC_PREFIXES = ["/api/v1/users", "/openapi.json", "/docs"]

async def jwt_auth_middleware(request: Request, call_next):
    path = request.url.path
    if any(path.startswith(p) for p in PUBLIC_PREFIXES):
        return await call_next(request)

    auth: str | None = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    token = auth.split(" ")[1]
    try:
        payload = decode_token(token)
        request.state.user_id = payload.get("sub")
        # Tenant ID is optional for backward compatibility
        request.state.tenant_id = payload.get("tenant_id")
    except Exception as exc:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return await call_next(request)
