from pydantic import BaseModel, Field
from datetime import datetime


class PriceHistoryBase(BaseModel):
    price: float = Field(..., gt=0)
    is_available: bool = True


class PriceHistoryCreate(PriceHistoryBase):
    product_id: int


class PriceHistoryResponse(PriceHistoryBase):
    id: int
    product_id: int
    checked_at: datetime
    
    class Config:
        from_attributes = True