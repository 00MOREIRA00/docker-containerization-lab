import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.exceptions import HttpAppError

logger = logging.getLogger(__name__)


def _message(detail: Any, fallback: str) -> str:
    """Retorna uma mensagem segura e consistente para o consumidor da API."""
    if isinstance(detail, str) and detail.strip():
        return detail
    return fallback


async def http_app_error_handler(
    request: Request,
    exc: HttpAppError,
) -> JSONResponse:
    """Trata as exceções HTTP customizadas da aplicação."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": _message(exc.detail, "Erro na aplicação")},
    )


async def starlette_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Trata erros HTTP gerados pelo FastAPI ou pelo Starlette."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": _message(exc.detail, "Erro HTTP")},
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Trata erros de validação de body, query string e parâmetros de rota."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": "Erro de validação dos parâmetros"},
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Trata exceções inesperadas sem expor detalhes internos da aplicação."""
    logger.exception("Erro não tratado durante a requisição", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Erro interno no servidor"},
    )
