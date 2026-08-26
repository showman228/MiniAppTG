from server.app.crud.order_crud import CRUDOrder
from server.app.crud.user_crud import CRUDUser
from server.app.schemas.order import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderUpdate,
)

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class OrderService:
    def __init__(self, db: AsyncSession):
        self.order_crud = CRUDOrder(db)
        self.user_crud = CRUDUser(db)

    async def get_all_orders(self) -> OrderListResponse:
        orders = await self.order_crud.get_all()
        order_responses = [OrderResponse.model_validate(order) for order in orders]
        total_price = sum(order.total_price for order in order_responses)
        return OrderListResponse(orders=order_responses, total_price=total_price)

    async def get_order_by_user_id(self, user_id: int) -> List[OrderResponse]:
        user = await self.user_crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found by user_id",
            )
        orders = await self.order_crud.get_by_user_id(user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_by_id(self, order_id: int) -> OrderResponse:
        order = await self.order_crud.get_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        return OrderResponse.model_validate(order)

    async def create_order(
        self, order_data: OrderCreate, user_id: int
    ) -> OrderResponse:
        order = await self.order_crud.create(order_data, user_id)
        return OrderResponse.model_validate(order)

    async def update_order(
        self, order_id: int, order_data: OrderUpdate
    ) -> OrderResponse:
        order = await self.order_crud.update(order_id, order_data)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found by order_id",
            )
        return OrderResponse.model_validate(order)

    async def delete_order(self, order_id: int) -> bool:
        order = await self.order_crud.delete(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found by order_id",
            )
        return True
