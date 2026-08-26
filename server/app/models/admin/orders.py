from sqladmin import ModelView
from server.app.models.order import Order

class OrdersAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.product_id,
        Order.quantity,
        Order.price,
        Order.total_price,
        Order.created_at
    ]