from pydantic import BaseModel
from app.schemas.ohlvc import OHLCV

class SignalResponse(BaseModel):
    instrument: str
    price: OHLCV
    direction: int
    isNewSignal: bool