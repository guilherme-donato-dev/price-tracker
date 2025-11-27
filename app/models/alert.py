from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AlertType(enum.Enum):
    PRICE_DROP = "price_drop"  # Quando preço cai
    TARGET_PRICE = "target_price"  # Quando atinge preço alvo
    BACK_IN_STOCK = "back_in_stock"  # Quando volta ao estoque


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    trigger_price = Column(Float, nullable=True)  # Preço que dispara o alerta
    message = Column(String, nullable=True)
    is_triggered = Column(Integer, default=False)  # Se alerta já foi enviado
    triggered_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="alerts")

    def __repr__(self):
        return f"<Alert(id={self.id}, product_id={self.product_id}, type={self.alert_type})>"