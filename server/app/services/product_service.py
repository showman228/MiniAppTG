from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.app.crud.category_crud import CRUDCategory
from server.app.crud.product_crud import CRUDProduct
from server.app.models import Product
from server.app.schemas.product import ProductCreate, ProductResponse, ProductListResponse


class ProductService:

    def __init__(self, db: AsyncSession):
        self.category_crud = CRUDCategory(db)
        self.product_crud = CRUDProduct(db)

    async def get_all_products(self) -> ProductListResponse:
        products = await self.product_crud.get_all_products()
        return [ProductResponse.model_validate(prod) for prod in products]

    async def get_products_by_category(self, category_id: int) -> ProductListResponse:
        category = await self.category_crud.get_by_id(category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by category_id")
        products = await self.product_crud.get_by_category_id(category_id)
        return [ProductResponse.model_validate(prod) for prod in products]

    async def get_by_id(self, product_id: int) -> ProductResponse:
        product = await self.product_crud.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found by product_id")
        return ProductResponse.model_validate(product)

    async def get_by_name(self, name: str) -> ProductResponse:
        product = await self.product_crud.get_by_name(name)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductResponse.model_validate(product)

    async def create(self, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_crud.get_by_id(product_data.category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        product = await self.product_crud.create(product_data)
        return ProductResponse.model_validate(product)

    async def update(self, product_id: int, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_crud.get_by_id(product_data.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by category_id")
        product = await self.product_crud.update(product_id, product_data)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found by product_id")
        return ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> bool:
        deleted = await self.product_crud.delete(product_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found by product_id")
        return True

