
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CanalStatus(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class CanalAmbiente(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class CanalBase(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    sistema_origem: str = Field(min_length=1)
    sistema_destino: str = Field(min_length=1)
    status: CanalStatus
    ambiente: CanalAmbiente


class CanalCreate(CanalBase):
    pass


class CanalUpdate(CanalBase):
    pass


class CanalResponse(CanalBase):
    id: UUID
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
