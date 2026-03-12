from server.app.models.order import Order
from server.app.schemas.order import OrderCreate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List

class CRUDOrder:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        order = await self.db.execute(select(Order).where(Order.id == order_id))
        return order.scalars().one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        order = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return list(order.scalars().all())

    async def get_all(self) -> List[Order]:
        orders = await self.db.execute(select(Order))
        return list(orders.scalars().all())

    async def create(self, order_data: OrderCreate) -> Optional[Order]:
        order = Order(
            user_id=order_data.user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            price=order_data.price,
            total_price=order_data.total_price
        )

        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)

        return order

    async def update(self, order_id: int, order_data: OrderCreate) -> Optional[Order]:
        order = await self.get_by_id(order_id)

        if order is None:
            return None

        for field, value in order_data.model_dump(exclude_unset=True).items():
            setattr(order, field, value)

        await self.db.commit()
        await self.db.refresh(order)

        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)

        if order is None:
            return False

        await self.db.delete(order)
        await self.db.commit()

        return True