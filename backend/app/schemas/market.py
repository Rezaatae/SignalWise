from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class OHLCV(BaseModel):
    timestamp: datetime
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)


class OHLCVSeries(BaseModel):
    symbol: str
    data: List[OHLCV]