import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Import the LegalAgent we created
from app.services.legal_agent import LegalAgent

router = APIRouter(prefix="/legal", tags=["legal"])


class GenerateRequest(BaseModel):
    policy_type: str  # e.g., "terms", "privacy", "cookies"
    context: dict = {}  # optional key/value pairs to interpolate


@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_policy(request: GenerateRequest):
    """Generate a legal policy document using Claude.

    The endpoint expects a ``policy_type`` indicating which kind of policy to
    generate and an optional ``context`` dictionary with additional information.
    It returns the generated text or raises a 500 error if the Anthropic SDK is
    unavailable or the API key is missing.
    """
    try:
        agent = LegalAgent()
    except Exception as e:
        # Could be missing API key or SDK not installed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:
        text = agent.generate(request.policy_type, request.context)
        return {"policy_type": request.policy_type, "content": text}
    except Exception as e:
        # Any error from the Claude API should be reported as server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate policy: {e}",
        )
