from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.exceptions import NotFoundError
from models.canais import CanalCreate, CanalUpdate
from models.canais_db import Canal


def create_canal(db: Session, dados: CanalCreate) -> Canal:
    canal = Canal(**dados.model_dump())
    db.add(canal)
    db.commit()
    db.refresh(canal)
    return canal


def list_canais(db: Session) -> list[Canal]:
    consulta = select(Canal).order_by(Canal.criado_em, Canal.id)
    return list(db.scalars(consulta).all())


def get_canal(db: Session, canal_id: UUID) -> Canal:
    canal = db.get(Canal, canal_id)
    if canal is None:
        raise NotFoundError("Canal não encontrado")
    return canal


def update_canal(db: Session, canal_id: UUID, dados: CanalUpdate) -> Canal:
    canal = get_canal(db, canal_id)
    for campo, valor in dados.model_dump().items():
        setattr(canal, campo, valor)
    db.commit()
    db.refresh(canal)
    return canal


def delete_canal(db: Session, canal_id: UUID) -> None:
    canal = get_canal(db, canal_id)
    db.delete(canal)
    db.commit()
