from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from server.app.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    image_url = Column(Text)

    category = relationship("Category", backref="products", lazy="selectin")

    def __repr__(self):
        return f"Product: {self.id}, name: {self.name}, description: {self.description}, price: {self.price}"
