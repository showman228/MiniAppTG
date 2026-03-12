from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from server.app.crud.product_crud import CRUDProduct
from server.app.schemas.cart import CartResponse, CartItem, CartItemUpdate, CartItemCreate

from fastapi import HTTPException, status

class CartService:

    def __init__(self, db: AsyncSession):
        self.product_crud = CRUDProduct(db)

    async def add_to_cart(self, item: CartItemCreate, cart_dict: Dict[int, int]) -> Dict[int, int]:
        product = await self.product_crud.get_by_id(item.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        if item.product_id in cart_dict:
            cart_dict[item.product_id] += item.quantity
        else:
            cart_dict[item.product_id] = item.quantity

        return cart_dict

    async def update_cart(self, cart_dict: Dict[int, int], item: CartItemCreate) -> Dict[int, int]:
        if item.product_id not in cart_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")
        cart_dict[item.product_id] = item.quantity
        return cart_dict

    async def remove_cart(self, product_id: int, cart_dict: Dict[int, int]) -> Dict[int, int]:
        if product_id not in cart_dict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")
        del cart_dict[product_id]
        return cart_dict

    async def get_details_of_cart(self, cart_dict: Dict[int, int]) -> CartResponse:
        if not cart_dict:
            return CartResponse(items=[], total=0, items_count=0)

        product_ids = list(cart_dict.keys())

        products = []
        for product_id in product_ids:
            product = await self.product_crud.get_by_id(product_id)
            products.append(product)

        products_dict = {product.id: product for product in products}

        cart_items = []
        total_price = 0.0
        items_count = 0

        for product_id, quantity in cart_dict.items():
            if product_id in products_dict:
                product = products_dict[product_id]
                subtotal = product.price * quantity

                cart_item = CartItem(
                    product_id=product_id,
                    name = product.name,
                    price = product.price,
                    quantity = quantity,
                    subtotal = subtotal,
                )

                cart_items.append(cart_item)
                total_price += subtotal
                items_count += quantity

        return CartResponse(
            items=cart_items,
            total=total_price,
            items_count=items_count
        )

