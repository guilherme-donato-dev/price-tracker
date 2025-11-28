from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from app.schemas.price_history import PriceHistoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., description="URL do produto")
    target_price: Optional[float] = Field(None, gt=0, description="Preço desejado para alerta")
    store: Optional[str] = Field(None, max_length=100)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = None
    target_price: Optional[float] = Field(None, gt=0)
    store: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    current_price: Optional[float]
    image_url: Optional[str]
    is_active: bool
    last_checked: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProductWithHistory(ProductResponse):
    price_history: List["PriceHistoryResponse"] = []
    
    class Config:
        from_attributes = True