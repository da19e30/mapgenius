"""Rutas CRUD para la entidad Cliente.

Se protege con JWT (dependencia get_current_user) y asegura que los recursos pertenezcan al tenant activo.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.client import Client
from app.models.user import User
from app.services.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/clients", tags=["clients"])

class ClientCreate(BaseModel):
    nit: str
    name: str
    email: str
    address: str | None = None
    tax_regime: str

class ClientRead(BaseModel):
    id: int
    nit: str
    name: str
    email: str
    address: str | None = None
    tax_regime: str

    class Config:
        orm_mode = True

@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verifica NIT único
    existing = db.query(Client).filter(Client.nit == client.nit).first()
    if existing:
        raise HTTPException(status_code=400, detail="NIT ya registrado")
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[ClientRead])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, client_in: ClientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for field, value in client_in.dict().items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(client)
    db.commit()
    return None