"""Security utilities: password hashing and JWT handling.

- Bcrypt via passlib for password storage.
- JWT creation/validation using python-jose.
"""

from datetime import datetime, timedelta
from typing import Any

from passlib.context import CryptContext
from jose import JWTError, jwt

from .config import settings

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------------------------------------------------------------
# JWT handling
# ---------------------------------------------------------------------------

def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
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
