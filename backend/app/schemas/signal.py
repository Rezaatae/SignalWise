from pydantic import BaseModel
from datetime import datetime

class SignalResponse(BaseModel):
    timestamp: datetime
    direction: int