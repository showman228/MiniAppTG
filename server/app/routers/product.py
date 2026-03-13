from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.database import get_db
from server.app.schemas.product import ProductResponse, ProductListResponse
from server.app.services.product_service import ProductService

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("/", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_all_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_by_id(product_id)

@router.get("/category/{category_id}", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def get_product_by_category_id(category_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_products_by_category(category_id)