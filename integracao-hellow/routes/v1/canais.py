from datetime import datetime, timezone
from uuid import uuid4, UUID

from fastapi import APIRouter, HTTPException

from models.canais import CanalCreate, CanalResponse, CanalUpdate

router = APIRouter(prefix="/canais/v1", tags=["canais"])

canais: list[CanalResponse] = []


@router.post("/", response_model=CanalResponse, status_code=201)
def create_canal(canal: CanalCreate):
    novo = CanalResponse(
        id=uuid4(),
        criado_em=datetime.now(timezone.utc),
        **canal.model_dump(),
    )
    canais.append(novo)
    return novo


@router.get("/", response_model=list[CanalResponse])
def list_canais():
    return canais


@router.get("/{canal_id}", response_model=CanalResponse)
def get_canal(canal_id: UUID):
    for canal in canais:
        if canal.id == canal_id:
            return canal
    raise HTTPException(status_code=404, detail="Canal não encontrado")


@router.put("/{canal_id}", response_model=CanalResponse)
def update_canal(canal_id: UUID, dados: CanalUpdate):
    for i, canal in enumerate(canais):
        if canal.id == canal_id:
            canais[i] = CanalResponse(
                id=canal.id,
                criado_em=canal.criado_em,
                **dados.model_dump(),
            )
            return canais[i]
    raise HTTPException(status_code=404, detail="Canal não encontrado")


@router.delete("/{canal_id}", status_code=204)
def delete_canal(canal_id: UUID):
    for i, canal in enumerate(canais):
        if canal.id == canal_id:
            canais.pop(i)
            return
    raise HTTPException(status_code=404, detail="Canal não encontrado")
