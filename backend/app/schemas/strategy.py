from pydantic import BaseModel
from datetime import datetime

class MACrossoverRequest(BaseModel):
    strategy_type: str
    fast_ma: int
    slow_ma: int
    asset: str
    start_date: datetime
    end_date: datetime
    initial_capital: int