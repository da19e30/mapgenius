"""Authentication routes: register, login, token refresh.

All endpoints return a ``Token`` schema containing access and refresh JWTs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.security import create_access_token, create_refresh_token, verify_password, decode_token, decode_without_verify
from datetime import datetime, timezone
from app.models.revoked_token import RevokedToken
from fastapi import Body
from app.db.session import get_db

router = APIRouter(prefix="/api/v1/users", tags=["auth"])

@router.post("/register", response_model=schemas.Token)
async def register_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # Verify email not already used
    existing = await crud.user.get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = await crud.user.create_user(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role.value,
    )
    access = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id})
    refresh = create_refresh_token({"sub": str(user.id), "tenant_id": user.tenant_id})
    return schemas.Token(access_token=access, refresh_token=refresh)

@router.post("/login", response_model=schemas.Token)
async def login_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.user.get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id})
    refresh = create_refresh_token({"sub": str(user.id), "tenant_id": user.tenant_id})
    return schemas.Token(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(payload: dict = Body(...), db: AsyncSession = Depends(get_db)):
    # Expect payload like {"refresh_token": "<token>"}
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="refresh_token missing")
    try:
        token_data = decode_token(refresh_token)
        user_id = token_data.get("sub")
        tenant_id = token_data.get("tenant_id")
        # If tenant_id not in token, fetch from DB
        if not tenant_id:
            from app.crud import user as user_crud
            user = await user_crud.get(db, int(user_id))
            if user:
                tenant_id = user.tenant_id
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    token_payload = {"sub": user_id}
    if tenant_id:
        token_payload["tenant_id"] = tenant_id
    access = create_access_token(token_payload)
    new_refresh = create_refresh_token(token_payload)
    return schemas.Token(access_token=access, refresh_token=new_refresh)

@router.post("/revoke", response_model=dict)
async def revoke_token(payload: dict = Body(...), db: AsyncSession = Depends(get_db)):
    """Revoke a refresh token.

    Expected payload: {"refresh_token": "<token>"}
    The token's ``jti`` and ``exp`` are stored in ``revoked_tokens``.
    """
    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="refresh_token missing")
    # Decode without verifying signature to read jti and exp
    try:
        payload_data = decode_without_verify(token)
        jti = payload_data.get("jti")
        exp_ts = payload_data.get("exp")
        if not jti or not exp_ts:
            raise ValueError("Missing jti or exp")
        expires_at = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token format")
    # Store revocation
    await crud.revoked_token.revoke(db, jti=jti, expires_at=expires_at)
    return {"detail": "Token revoked"}
