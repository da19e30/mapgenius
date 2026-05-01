"""
Endpoints de autenticación: registro y login con JWT.

Este módulo expone:
- POST /register: crear nueva cuenta de usuario
- POST /login: autenticar y obtener JWT (access token)
- GET /me: (protegido) obtener información del usuario actual
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.services.auth import hash_password, verify_password
from app.services.jwt import create_access_token, get_current_user
from app.services.email import send_welcome_email, send_admin_notification
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])


# Esquemas de entrada (Pydantic)
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario:
    - Valida unicidad de email y username
    - Hashea la contraseña con bcrypt
    - Guarda en base de datos
    """
    # Verificar email duplicado
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    # Verificar username duplicado
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    hashed_pw = hash_password(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Enviar correos de notificación (no bloquea si falla)
    try:
        send_welcome_email(new_user.email, new_user.username)
    except Exception as e:
        print(f"[EMAIL] Welcome email failed: {e}")
    try:
        send_admin_notification(new_user.email, new_user.username, new_user.id)
    except Exception as e:
        print(f"[EMAIL] Admin notification failed: {e}")

    return {
        "message": "Usuario registrado exitosamente",
        "user_id": new_user.id,
        "email": new_user.email,
    }


@router.post("/login", response_model=TokenResponse)
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica al usuario y devuelve un JWT válido por 30 minutos.

    - Busca por email
    - Verifica contraseña con bcrypt
    - Genera token con claim 'sub' = email
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30),
    )
    return {"access_token": access_token, "token_type": "bearer", "email": user.email}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint protegido: devuelve información del usuario autenticado.

    Requiere header: Authorization: Bearer <token>
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }

# ----------- User profile update -----------
class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None

@router.put("/profile")
async def update_profile(update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Actualiza username y/o email del usuario autenticado."""
    if update.username:
        # verificar unicidad
        if db.query(User).filter(User.username == update.username, User.id != current_user.id).first():
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        current_user.username = update.username
    if update.email:
        if db.query(User).filter(User.email == update.email, User.id != current_user.id).first():
            raise HTTPException(status_code=400, detail="El email ya está en uso")
        current_user.email = update.email
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"message": "Perfil actualizado", "username": current_user.username, "email": current_user.email}

# ----------- Change password -----------
class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password")
async def change_password(payload: PasswordChange, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Cambia la contraseña del usuario después de validar la actual."""
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    current_user.password = hash_password(payload.new_password)
    db.add(current_user)
    db.commit()
    return {"message": "Contraseña actualizada correctamente"}

# ----------- Delete account -----------
@router.delete("/delete")
async def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Elimina la cuenta del usuario autenticado y sus datos asociados (cascada)."""
    db.delete(current_user)
    db.commit()
    return {"message": "Cuenta eliminada"}

# ---------- Username / Email availability checks ----------
@router.get("/check-username")
async def check_username(username: str, db: Session = Depends(get_db)):
    """Devuelve `true` si el nombre de usuario está disponible."""
    exists = db.query(User).filter(User.username == username).first()
    return {"available": not bool(exists)}

@router.get("/check-email")
async def check_email(email: str, db: Session = Depends(get_db)):
    """Devuelve `true` si el email está disponible."""
    exists = db.query(User).filter(User.email == email).first()
    return {"available": not bool(exists)}

