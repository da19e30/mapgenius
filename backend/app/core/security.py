"""Security utilities: password hashing and JWT handling.

- Bcrypt via passlib for password storage.
- JWT creation/validation using python-jose.
"""

from datetime import datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from .config import settings

# ---------------------------------------------------------------------------
# Password hashing (using bcrypt directly)
# ---------------------------------------------------------------------------
import bcrypt


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ---------------------------------------------------------------------------
# JWT handling
# ---------------------------------------------------------------------------

import uuid

def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    # Ensure a unique JWT ID (jti) for revocation tracking
    if "jti" not in data:
        data["jti"] = str(uuid.uuid4())
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    secret = settings.JWT_SECRET_KEY.get_secret_value()
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: dict[str, Any]) -> str:
    return _create_token(subject, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(subject: dict[str, Any]) -> str:
    return _create_token(subject, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as exc:
        raise exc  # Caller will translate to HTTPException


def decode_without_verify(token: str) -> dict[str, Any]:
    """Decode a JWT without signature verification.
    Useful for extracting ``jti`` and ``exp`` when we only need to check revocation.
    """
    # jose.jwt requires a key even when skipping verification; empty string works.
    return jwt.decode(token, "", options={"verify_signature": False})
