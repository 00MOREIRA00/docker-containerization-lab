from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.exceptions import HttpAppError
from handlers.handlers import (
    http_app_error_handler,
    starlette_http_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)
from routes.v1.canais import router as hellow_router

app = FastAPI()

app.include_router(hellow_router)
app.add_exception_handler(HttpAppError, http_app_error_handler)
app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)
