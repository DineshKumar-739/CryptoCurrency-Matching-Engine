from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from datetime import datetime

class Order(BaseModel):
    symbol: str
    order_type: str
    side: str
    quantity: float
    price: Optional[float] = None
    order_id: str = str(uuid4())
    timestamp: str = datetime.utcnow().isoformat()

class Trade(BaseModel):
    trade_id: str
    symbol: str
    price: float
    quantity: float
    aggressor_side: str
    maker_order_id: str
    taker_order_id: str
    timestamp: str
