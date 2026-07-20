from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from pydantic import BaseModel, Field

from server.app.database import get_db
from server.app.services.cart_service import CartService
from server.app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart: Dict[int, int] = {}

class UpdateCartRequest(AddToCartRequest):
    pass

class RemoveFromCartRequest(BaseModel):
    product_id: int
    cart: Dict[int, int] = {}

class CartDetailsRequest(BaseModel):
    cart_data: Dict[int, int] = Field(default_factory=dict, description="product_id → quantity")

@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=CartResponse)
async def add_to_cart(request: AddToCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    item = CartItemCreate(
        product_id=request.product_id,
        quantity=request.quantity
    )
    updated_cart = await service.add_to_cart(cart_dict=request.cart, item=item)
    return await service.get_details_of_cart(updated_cart)

@router.post("/details", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart_details(body: CartDetailsRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.get_details_of_cart(body.cart_data)

@router.put("/update", status_code=status.HTTP_200_OK, response_model=CartResponse)
async def update_cart(request: UpdateCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    item = CartItemUpdate(
        product_id=request.product_id,
        quantity=request.quantity
    )
    updated_cart = await service.update_cart(cart_dict=request.cart, item=item)
    return {"cart": updated_cart}

@router.post("/remove", status_code=status.HTTP_200_OK, response_model=CartResponse)
async def remove_from_cart(request: RemoveFromCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    updated_cart = await service.remove_cart(product_id=request.product_id, cart_dict=request.cart)
    return await service.get_details_of_cart(updated_cart)