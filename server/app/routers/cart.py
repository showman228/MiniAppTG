from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from pydantic import BaseModel

from server.app.database import get_db
from server.app.services.cart_service import CartService
from server.app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate


router = APIRouter(
    prefix="/api/cart",
    tags=["cart"]
)

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart: Dict[int, int] = {}

class UpdateCartRequest(AddToCartRequest):
    pass

class RemoveFromCartRequest(BaseModel):
    cart: Dict[int, int] = {}

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_to_cart(request: AddToCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    item = CartItemCreate(
        product_id=request.product_id,
        quantity=request.quantity
    )
    update_cart = await service.add_to_cart(cart_dict=request.cart, item=item)
    return {"cart": update_cart}

@router.post("/details", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(cart_data: Dict[int, int], db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.get_details_of_cart(cart_data)

@router.put("/update", status_code=status.HTTP_200_OK, response_model=CartResponse)
async def update_cart(request: UpdateCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    item = CartItemUpdate(
        product_id=request.product_id,
        quantity=request.quantity
    )
    updated_cart = await service.update_cart(cart_dict=request.cart, item=item)
    return {"cart": updated_cart}

@router.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(product_id: int, request: RemoveFromCartRequest, db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    update_cart = await service.remove_cart(product_id=product_id, cart_dict=request.cart)
    return {"cart": update_cart}