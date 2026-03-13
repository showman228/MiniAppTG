from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.app.services.category_service import CategoryService
from server.app.schemas.category import CategoryResponse
from server.app.database import get_db

router = APIRouter(
    prefix="/api/category",
    tags=["category"]
)

@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_all()


@router.get("/{category_id}",response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_by_id(category_id)

