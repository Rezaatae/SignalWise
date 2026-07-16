from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class EquityCurve(BaseModel):
    timestamp: datetime
    equity: Optional[float]


class BacktestResult(BaseModel):
    ec: Optional[List[EquityCurve]]
    daily_vol: Optional[float]
    daily_returns: Optional[List[float]]
    vol: Optional[float]
    # sharpe: Optional[float]
    # drawdown: Optional[float]
