from fastapi import APIRouter
from app.api.v1.endpoints import maCrossover

api_router = APIRouter()
api_router.include_router(maCrossover.router, prefix="/run-backtest")