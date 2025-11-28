from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.alert import AlertType


class AlertBase(BaseModel):
    alert_type: AlertType
    trigger_price: Optional[float] = Field(None, gt=0)
    message: Optional[str] = None


class AlertCreate(AlertBase):
    product_id: int


class AlertResponse(AlertBase):
    id: int
    product_id: int
    is_triggered: bool
    triggered_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True