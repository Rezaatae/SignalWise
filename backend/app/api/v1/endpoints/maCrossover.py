from fastapi import APIRouter
from app.schemas.strategy import MACrossoverRequest
from app.services.backtest.backtest import Backtest

router = APIRouter()

@router.post("/ma-crossover/{instrument}")
def run_ma_crossover(instrument: str, MACrossoverConfig: MACrossoverRequest):
    bt = Backtest(instrument=instrument, strategyType="MACrossover", strategyConfig=MACrossoverConfig)
    return bt.run()