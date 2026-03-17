from sqladmin import ModelView
from server.app.models.order import Order

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.product_id, Order.price, Order.quantity, Order.total_price, Order.user_id, Order.created_at]
    column_filters = ["id", "price", "quantity", "total_price", "user_id", "created_at"]
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-box"