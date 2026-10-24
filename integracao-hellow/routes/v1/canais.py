from datetime import datetime, timezone
from uuid import uuid4, UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.canais import CanalCreate, CanalResponse, CanalUpdate
from models.canais_db import Canal
from provider.database import get_db

router = APIRouter(prefix="/canais/v1", tags=["canais"])

@router.post("/", response_model=CanalResponse, status_code=201)
def create_canal(canal: CanalCreate, db: Session = Depends(get_db)):
    novo = Canal(**canal.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.get("/", response_model=list[CanalResponse])
def list_canais(db: Session = Depends(get_db)):
    consulta = select(Canal).order_by(Canal.criado_em, Canal.id)
    return db.scalars(consulta).all()


@router.get("/{canal_id}", response_model=CanalResponse)
def get_canal(canal_id: UUID, db: Session = Depends(get_db)):
    canal = db.get(Canal, canal_id)

    if canal is None:
        raise HTTPException(status_code=404, detail="Canal não encontrado")

    return canal


@router.put("/{canal_id}", response_model=CanalResponse)
def update_canal(canal_id: UUID, dados: CanalUpdate, db: Session = Depends(get_db)):
    canal = db.get(Canal, canal_id)

    if canal is None:
        raise HTTPException(status_code=404, detail="Canal não encontrado")

    for campo, valor in dados.model_dump().items():
        setattr(canal, campo, valor)

    db.commit()
    db.refresh(canal)

    return canal


@router.delete("/{canal_id}", status_code=204)
def delete_canal(canal_id: UUID, db: Session = Depends(get_db)):
    canal = db.get(Canal, canal_id)

    if canal is None:
        raise HTTPException(status_code=404, detail="Canal não encontrado")

    db.delete(canal)
    db.commit()
