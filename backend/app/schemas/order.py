from datetime import datetime
from enum import StrEnum
from uuid import uuid4
from app.schemas.ohlvc import OHLCV
from typing import List
from pydantic import BaseModel, Field

class Position(BaseModel):
    instrument: str

    quantity: int

    marketPrice: float

    costHistory: List[float]

    @property
    def averageCost(self) -> float:
        return sum(self.costHistory)/len(self.costHistory) if self.costHistory else 0

    @property
    def marketValue(self):
        return self.quantity*self.marketPrice

    @property
    def costBasis(self):
        return self.quantity*self.averageCost

    @property
    def unrealizedPnL(self):
        return self.marketValue - self.costBasis


class OrderType(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class OrderStatus(StrEnum):
    NEW = "NEW"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid4()))

    instrument: str
    
    order_type: OrderType

    quantity: int

    created_at: datetime

    filled_quantity: int = 0

    status: OrderStatus = OrderStatus.NEW

    @property
    def remaining_quantity(self) -> int:
        return self.quantity - self.filled_quantity
    
class Quote(BaseModel):
    instrument: str

    timestamp: datetime

    bid: float
    ask: float

    available_bid_size: int
    available_ask_size: int

class Fill(BaseModel):
    order_id: str

    order_type: str

    instrument: str

    quantity: int

    price: float

    commission: float

    timestamp: datetime

class ExecutionReport(BaseModel):
    order_id: str

    status: OrderStatus

    filled_quantity: int

    remaining_quantity: int

    average_fill_price: float | None = None

    timestamp: datetime