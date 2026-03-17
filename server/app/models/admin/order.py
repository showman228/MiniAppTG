from sqladmin import ModelView
from server.app.models.order import Order

class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.product_id,
        Order.quantity,
        Order.price,
        Order.total_price,
        Order.created_at
    ]

    # column_details_list = [
    #     Order.id,
    #     Order.user_id,
    #     Order.product_id,
    #     Order.quantity,
    #     Order.price,
    #     Order.total_price,
    #     Order.created_at
    # ]
    #
    # column_sortable_list = [
    #     Order.id,
    #     Order.created_at,
    #     Order.total_price
    # ]

    # column_filters = ["name", "price", "category_id", "created_at"]  # ✅ строки

    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-cart-shopping"