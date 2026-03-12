from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class OrderBase(BaseModel):
    user_id: int = Field(..., description="user id")
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Кол-во товаров")
    price: int = Field(..., gt=0, description="Цена за товар")
    total_price: int = Field(..., gt=0, description="Общая сумма товаров")

class OrderCreate(OrderBase):
    pass

class OrderResponse(BaseModel):
    id: int = Field(..., description="Order ID")
    user_id: int
    product_id: int = Field(..., description="Product ID")
    quantity: int
    price: int = Field(..., gt=0, description="Цена за товар")
    total_price: int = Field(..., description="кол-во * ценик_товара")
    created_at: datetime

    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total_price: int = Field(..., gt=0, description="Ценик за все товары")

