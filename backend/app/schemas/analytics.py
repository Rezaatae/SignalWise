from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class EquityCurve(BaseModel):
    timestamp: datetime
    equity: float


class BacktestResult(BaseModel):
    ec: List[EquityCurve]
    sharpe: float
    drawdown: float
    vol: float
