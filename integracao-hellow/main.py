from fastapi import FastAPI, APIRouter
import uvicorn

from routes.v1.canais import router as hellow_router

app = FastAPI()
router = APIRouter()

app.include_router(hellow_router)
