import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Placeholder URLs – replace with real OAuth client IDs/secrets in production
GOOGLE_OAUTH_URL = os.getenv("GOOGLE_OAUTH_URL")
MICROSOFT_OAUTH_URL = os.getenv("MICROSOFT_OAUTH_URL")

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth flow (placeholder)."""
    if not GOOGLE_OAUTH_URL:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured",
        )
    return RedirectResponse(url=GOOGLE_OAUTH_URL)

@router.get("/microsoft")
async def microsoft_login():
    """Redirect to Microsoft OAuth flow (placeholder)."""
    if not MICROSOFT_OAUTH_URL:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Microsoft OAuth not configured",
        )
    return RedirectResponse(url=MICROSOFT_OAUTH_URL)
