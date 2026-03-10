from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class OrderBase(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., ge=0, description="Кол-во товаров")
    price: int = Field(..., gt=0, description="Цена за товар")
    total_price: int = Field(..., ge=0, description="Общая сумма товаров")
    created_at: datetime = Field(..., description="Когда заказали товар")


class OrderCreate(OrderBase):
    pass

class OrderResponse(BaseModel):
    id: int = Field(..., description="Order ID")
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

