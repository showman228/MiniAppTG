from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.app.core.auth import get_current_user
from server.app.models.user import User

from server.app.database import get_db
from server.app.services.order_service import OrderService
from server.app.schemas.order import OrderListResponse, OrderResponse, OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.create_order(order_data, current_user.id)

@router.put("/update/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.update_order(order_id, order_data)

@router.delete("/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    await service.delete_order(order_id)

@router.get("/", response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.get_all_orders()

@router.get("/users/{user_id}", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view another user's orders")
    service = OrderService(db)
    return await service.get_order_by_user_id(user_id)

@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.get_by_id(order_id)
