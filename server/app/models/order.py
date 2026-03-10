from server.app.database import Base
from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from  sqlalchemy import Integer, Column, ForeignKey, DateTime

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    product = relationship("Product", backref="orders")
    user = relationship("User", backref="orders")

    def __repr__(self):
        return f"Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity})"