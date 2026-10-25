from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from models.canais import CanalCreate, CanalResponse, CanalUpdate
from provider.database import get_db
from service import canais as canais_service

router = APIRouter(prefix="/canais/v1", tags=["canais"])


@router.post("/", response_model=CanalResponse, status_code=201)
def create_canal(canal: CanalCreate, db: Session = Depends(get_db)):
    return canais_service.create_canal(db, canal)


@router.get("/", response_model=list[CanalResponse])
def list_canais(db: Session = Depends(get_db)):
    return canais_service.list_canais(db)


@router.get("/{canal_id}", response_model=CanalResponse)
def get_canal(canal_id: UUID, db: Session = Depends(get_db)):
    return canais_service.get_canal(db, canal_id)


@router.put("/{canal_id}", response_model=CanalResponse)
def update_canal(canal_id: UUID, dados: CanalUpdate, db: Session = Depends(get_db)):
    return canais_service.update_canal(db, canal_id, dados)


@router.delete("/{canal_id}", status_code=204)
def delete_canal(canal_id: UUID, db: Session = Depends(get_db)):
    canais_service.delete_canal(db, canal_id)
