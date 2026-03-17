from server.app.models.order import Order
from sqladmin import ModelView

class OrderAdmin(ModelView):
    column_list = [Order.id, Order.product, Order.price, Order.quantity, Order.total_price, Order.user_id, Order.created_at]
    column_filters = ["id", "product", "price", "quantity", "total_price", "user_id", "created_at"]
    name = "Заказы"
    name_plural = "Заказы"
    icon = "fa-solid fa-cart-shopping"