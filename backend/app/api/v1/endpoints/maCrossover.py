from fastapi import APIRouter
from app.schemas.strategy import MACrossoverRequest
from app.services.backtest.backtest import Backtest

router = APIRouter()

@router.post("/ma-crossover/{MACrossoverConfig}")
async def run_ma_crossover(MACrossoverConfig: MACrossoverRequest):
    bt = Backtest("MACrossover", strategyConfig=MACrossoverConfig)
    return await bt.run()