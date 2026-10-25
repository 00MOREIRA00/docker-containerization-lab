import unittest

from pydantic import ValidationError

from models.canais import CanalAmbiente, CanalCreate, CanalStatus


class CanalModelTests(unittest.TestCase):
    def test_rejeita_nome_muito_curto(self):
        with self.assertRaises(ValidationError):
            CanalCreate(
                nome="ab",
                sistema_origem="loja",
                sistema_destino="erp",
                status=CanalStatus.ATIVO,
                ambiente=CanalAmbiente.DEV,
            )

    def test_rejeita_status_invalido(self):
        with self.assertRaises(ValidationError):
            CanalCreate(
                nome="Pedidos",
                sistema_origem="loja",
                sistema_destino="erp",
                status="pausado",
                ambiente=CanalAmbiente.DEV,
            )
