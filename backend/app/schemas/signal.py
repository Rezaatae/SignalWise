from pydantic import BaseModel
from app.schemas.ohlvc import OHLCV

class SignalResponse(BaseModel):
    instrument: str
    sharePrice: OHLCV
    direction: int
    isNewSignal: bool