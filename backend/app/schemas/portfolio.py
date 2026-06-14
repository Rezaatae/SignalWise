from pydantic import BaseModel
from app.schemas.ohlvc import OHLCV

class Position(BaseModel):
    instrument: str
    allocation: int
    price: OHLCV

class Order(BaseModel):
    orderType: str
    instrument: str
    shares: int
    price: OHLCV