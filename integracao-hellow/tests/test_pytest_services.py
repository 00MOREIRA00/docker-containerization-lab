import os
from uuid import UUID

import pytest

os.environ.setdefault("POSTGRES_PASSWORD", "test-password")

from exceptions.exceptions import NotFoundError
from models.canais import CanalAmbiente, CanalCreate, CanalStatus
from service import canais


def canal_valido():
    return CanalCreate(
        nome="Pedidos",
        sistema_origem="loja",
        sistema_destino="erp",
        status=CanalStatus.ATIVO,
        ambiente=CanalAmbiente.DEV,
    )


def test_pytest_fixture_persiste_canal(db_session):
    canais.create_canal(db_session, canal_valido())

    assert len(canais.list_canais(db_session)) == 1


def test_pytest_verifica_excecao_de_canal_inexistente(db_session):
    with pytest.raises(NotFoundError):
        canais.get_canal(
            db_session,
            UUID("00000000-0000-0000-0000-000000000000"),
        )
