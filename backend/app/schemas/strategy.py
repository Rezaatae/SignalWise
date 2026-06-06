from pydantic import BaseModel
from datetime import datetime

class MACrossoverRequest(BaseModel):
    strategy_type: str
    fast_ma_window: int
    slow_ma_window: int
    instrument: str
    start_date: datetime
    end_date: datetime
    initial_capital: int