from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.app.database import get_db
from server.app.services.order_service import OrderService
from server.app.schemas.order import OrderListResponse, OrderResponse, OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/api/order",
    tags=["order"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.create_order(order_data)

@router.put("/update/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order_data: OrderUpdate, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.update_order(order_id, order_data)

@router.delete("/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.delete_order(order_id)

@router.get("/", response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_orders(db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_all_orders()

@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_by_id(order_id)

@router.get("/users/{user_id}", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_order_by_user_id(user_id)