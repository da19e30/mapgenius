"""User API endpoints.

Provides HTTP handlers for user registration, login and profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)
from app.services.user_service import UserService
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    settings: Settings = Depends(get_settings),
    service: UserService = Depends(UserService),
) -> UserResponse:
    """Create a new user.

    Args:
        payload: Data required to create a user.
        settings: Application settings (unused, injected for future use).
        service: Business‑logic service.
    """
    try:
        user = await service.create_user(payload)
        return UserResponse.from_orm(user)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(UserService),
) -> TokenResponse:
    """Authenticate a user and return a JWT token."""
    token = await service.authenticate_user(form_data.username, form_data.password)
    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user=Depends(UserService.get_current_user),
) -> UserResponse:
    """Return the currently authenticated user."""
    return UserResponse.from_orm(current_user)
