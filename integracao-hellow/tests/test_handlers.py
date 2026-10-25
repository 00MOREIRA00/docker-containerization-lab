import json
import asyncio
import unittest

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.exceptions import NotFoundError
from handlers.handlers import (
    http_app_error_handler,
    starlette_http_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)


def response_json(response):
    return json.loads(response.body)


class HandlerTests(unittest.TestCase):
    def test_trata_excecao_customizada(self):
        response = asyncio.run(
            http_app_error_handler(None, NotFoundError("Canal não encontrado"))
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json(response),
            {"message": "Canal não encontrado"},
        )

    def test_trata_excecao_http_do_starlette(self):
        response = asyncio.run(
            starlette_http_exception_handler(
                None,
                StarletteHTTPException(status_code=405, detail="Método não permitido"),
            )
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response_json(response),
            {"message": "Método não permitido"},
        )

    def test_usa_mensagem_padrao_quando_erro_http_nao_tem_detalhe(self):
        response = asyncio.run(
            starlette_http_exception_handler(
                None,
                StarletteHTTPException(status_code=404, detail=""),
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json(response), {"message": "Erro HTTP"})

    def test_trata_erro_de_validacao(self):
        exc = RequestValidationError(
            [
                {
                    "type": "missing",
                    "loc": ("body", "nome"),
                    "msg": "Field required",
                    "input": {},
                }
            ]
        )

        response = asyncio.run(validation_exception_handler(None, exc))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response_json(response),
            {"message": "Erro de validação dos parâmetros"},
        )

    def test_trata_erro_inesperado_sem_expor_detalhes(self):
        response = asyncio.run(
            unexpected_exception_handler(None, RuntimeError("detalhe interno"))
        )

        self.assertEqual(response.status_code, 500)
        self.assertNotIn("detalhe interno", response_json(response)["message"])


if __name__ == "__main__":
    unittest.main()
