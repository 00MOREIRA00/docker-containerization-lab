import os
import unittest
from uuid import uuid4

os.environ.setdefault("POSTGRES_PASSWORD", "test-password")

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from exceptions.exceptions import NotFoundError
from models.canais import CanalAmbiente, CanalCreate, CanalStatus, CanalUpdate
from models.canais_db import Canal
from provider.database import Base
from service import canais


class CanalServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    @staticmethod
    def dados(nome="Pedidos"):
        return CanalCreate(
            nome=nome,
            sistema_origem="loja",
            sistema_destino="erp",
            status=CanalStatus.ATIVO,
            ambiente=CanalAmbiente.DEV,
        )

    def test_cria_e_lista_canal(self):
        criado = canais.create_canal(self.session, self.dados())

        resultado = canais.list_canais(self.session)

        self.assertIsNotNone(criado.id)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nome, "Pedidos")

    def test_busca_canal_inexistente_levanta_not_found(self):
        with self.assertRaises(NotFoundError):
            canais.get_canal(self.session, uuid4())

    def test_atualiza_canal(self):
        criado = canais.create_canal(self.session, self.dados())
        dados = CanalUpdate(
            nome="Pedidos atualizados",
            sistema_origem="loja",
            sistema_destino="erp",
            status=CanalStatus.INATIVO,
            ambiente=CanalAmbiente.STAGING,
        )

        atualizado = canais.update_canal(self.session, criado.id, dados)

        self.assertEqual(atualizado.nome, "Pedidos atualizados")
        self.assertEqual(atualizado.status, CanalStatus.INATIVO.value)
        self.assertEqual(atualizado.ambiente, CanalAmbiente.STAGING.value)

    def test_atualiza_canal_inexistente_levanta_not_found(self):
        with self.assertRaises(NotFoundError):
            canais.update_canal(self.session, uuid4(), self.dados("Atualizado"))

    def test_exclui_canal(self):
        criado = canais.create_canal(self.session, self.dados())

        canais.delete_canal(self.session, criado.id)

        with self.assertRaises(NotFoundError):
            canais.get_canal(self.session, criado.id)

    def test_exclui_canal_inexistente_levanta_not_found(self):
        with self.assertRaises(NotFoundError):
            canais.delete_canal(self.session, uuid4())


if __name__ == "__main__":
    unittest.main()
