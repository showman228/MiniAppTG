from server.app.models import Category
from server.app.models.product import Product
from server.app.schemas.product import ProductCreate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List


class CRUDProduct:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self) -> List[Product]:  # Для админки
        product = await self.db.execute(
            select(Product)
            .options(selectinload(Product.category))
            .limit(100)
        )
        return list(product.scalars().all())

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        product = await self.db.execute(select(Product).where(Product.id == product_id))
        return product.scalars().one_or_none()

    async def get_by_ids(self, product_ids: List[int]) -> List[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Optional[Product]:
        product = await self.db.execute(select(Product).where(Product.name == name))
        return product.scalars().one_or_none()

    async def get_by_category_id(self, category_id: int) -> List[Product]:
        product = await self.db.execute(select(Product).where(Product.category_id == category_id))
        return list(product.scalars().all())

    async def create(self, product_data: ProductCreate) -> Optional[Product]:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category_id=product_data.category_id
        )

        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product_id: int, product_data: ProductCreate) -> Optional[Product]:
        product = await self.get_by_id(product_id)

        if not product:
            return None

        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        await self.db.commit()
        await self.db.refresh(product)

        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if not product:
            return False

        await self.db.delete(product)
        await self.db.commit()
        return True


