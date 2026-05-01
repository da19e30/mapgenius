"""
Servicio de autenticación JWT para Mapgenius Solutions.

Este módulo:
- Genera tokens de acceso firmados (HS256)
- Decodifica y valida tokens entrantes
- Extrae el usuario actual desde el token (dependency para FastAPI)
- Define el esquema de seguridad OAuth2 Bearer
- Hash y verificación de contraseñas con bcrypt
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.core.security import decode_without_verify
from app.crud.revoked_token import is_revoked

# Contexto de hash para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

# Configuración desde variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey1234567890")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Esquema OAuth2: el cliente debe enviar: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT con los datos proporcionados y tiempo de expiración.

    Parámetros:
    - data: diccionario con claims (usualmente {"sub": user_email})
    - expires_delta: tiempo de expiración opcional

    Retorna:
    - str: token JWT firmado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodifica y valida un JWT. Lanza JWTError si es inválido o expiró.

    Parámetros:
    - token: string del JWT

    Retorna:
    - dict: payload decodificado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency de FastAPI para obtener el usuario autenticado desde el JWT.

    Uso:
        @app.get("/protected")
        def r(current_user: User = Depends(get_current_user)):
            ...

    Lanza:
    - HTTPException 401 si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Check revocation using jti claim (if present)
        jti = payload.get("jti")
        if jti:
            rev = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
            if rev:
                raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
