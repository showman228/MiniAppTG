from server.app.routers.order import router as order_router
from server.app.routers.product import router as product_router
from server.app.routers.category import router as category_router
from server.app.routers.cart import router as cart_router
from server.app.routers.user import router as user_router

__all__ = ["order_router", "product_router",
           "category_router", "cart_router", "user_router"]
