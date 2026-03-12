from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List

from server.app.crud.category_crud import CRUDCategory
from server.app.schemas.category import CategoryResponse, CategoryCreate

class CategoryService:
    def __init__(self, crud: AsyncSession):
        self.crud = CRUDCategory(crud)

    async def get_all(self) -> List[CategoryResponse]:
        category = await self.crud.get_all()
        return [CategoryResponse.model_validate(cat) for cat in category]

    async def get_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.crud.get_by_id(category_id)

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by category_id")

        return CategoryResponse.model_validate(category)

    async def get_by_name(self, name: str) -> CategoryResponse:
        category = await self.crud.get_by_name(name)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by name")
        return CategoryResponse.model_validate(category)

    async def get_by_slug(self, slug: str) -> CategoryResponse:
        category = await self.crud.get_by_slug(slug)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by slug")
        return CategoryResponse.model_validate(category)

    async def create(self, category_data: CategoryCreate) -> CategoryResponse:
        existing = await self.crud.get_by_name(category_data.name)
        if existing:
            raise HTTPException(status_code=409, detail="Category already exists")
        category = await self.crud.create(category_data)
        return CategoryResponse.model_validate(category)

    async def update(self, category_id: int, data: CategoryCreate) -> CategoryResponse:
        category = await self.crud.update(category_id, data)

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by category_id")

        return CategoryResponse.model_validate(category)

    async def delete(self, category_id: int) -> bool:
        category = await self.crud.delete(category_id)

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found by category_id")

        return True