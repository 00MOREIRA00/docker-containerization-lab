from fastapi import HTTPException, status


class HttpAppError(HTTPException):
    """## Exceção HTTP padronizada da aplicação

    Classe base utilizada para criar erros HTTP customizados dentro da aplicação,
    garantindo consistência na estrutura e na formatação das respostas enviadas ao
    consumidor.

    Args:
        status_code (int): O código HTTP correspondente ao erro ocorrido.
        detail (str): A mensagem descritiva do erro, destinada ao consumidor.

    Raises:
        HttpAppError: Sempre que um erro HTTP customizado precisar ser lançado pela aplicação.
    """
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


# EXCEÇÕES 4XX
class BadRequestError(HttpAppError):
    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)

class UnauthorizedError(HttpAppError):
    def __init__(self, detail: str = "Não autorizado"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)

class ForbiddenError(HttpAppError):
    def __init__(self, detail: str = "Acesso proibido"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)

class NotFoundError(HttpAppError):
    def __init__(self, detail: str = "Não encontrado"):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)

class MethodNotAllowedError(HttpAppError):
    def __init__(self, detail: str = "Método não permitido"):
        super().__init__(status.HTTP_405_METHOD_NOT_ALLOWED, detail)

class ConflictError(HttpAppError):
    def __init__(self, detail: str = "Conflito na requisição"):
        super().__init__(status.HTTP_409_CONFLICT, detail)

class PreconditionFailedError(HttpAppError):
    def __init__(self, detail: str = "Condição obrigatória não atendida"):
        super().__init__(status.HTTP_412_PRECONDITION_FAILED, detail)

class UnprocessableEntityError(HttpAppError):
    def __init__(self, detail: str = "Erro de validação de dados"):
        super().__init__(status.HTTP_422_UNPROCESSABLE_CONTENT, detail)

class TooManyRequestsError(HttpAppError):
    def __init__(self, detail: str = "Muitas requisições. Tente novamente mais tarde."):
        super().__init__(status.HTTP_429_TOO_MANY_REQUESTS, detail)


# EXCEÇÕES 5XX
class InternalServerError(HttpAppError):
    def __init__(self, detail: str = "Erro interno no servidor"):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)

class NotImplementedHTTPError(HttpAppError):  # renomeado p/ não colidir com built-in
    def __init__(self, detail: str = "Funcionalidade não implementada"):
        super().__init__(status.HTTP_501_NOT_IMPLEMENTED, detail)

class BadGatewayError(HttpAppError):
    def __init__(self, detail: str = "Erro no processamento da requisição"):
        super().__init__(status.HTTP_502_BAD_GATEWAY, detail)

class ServiceUnavailableError(HttpAppError):
    def __init__(self, detail: str = "Serviço indisponível"):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, detail)

class GatewayTimeoutError(HttpAppError):
    def __init__(self, detail: str = "Tempo de resposta do servidor esgotado"):
        super().__init__(status.HTTP_504_GATEWAY_TIMEOUT, detail)
