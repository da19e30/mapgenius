"""Health‑check router.
Provides a simple endpoint to verify the API is up and running.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["utility"])

@router.get("/health", tags=["utility"])
async def health_check() -> dict:
    """Return a basic health status.

    Returns:
        dict: JSON with a ``status`` key set to ``"ok"``.
    """
    return {"status": "ok", "message": "Mapgenius API está operativa"}
