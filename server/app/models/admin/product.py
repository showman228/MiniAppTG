from server.app.models.product import Product
from sqladmin import ModelView

# 3. Описываем таблицу Товаров
class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.name,
        Product.price,
        Product.description,
        Product.category_id,
        Product.created_at
    ]

    # column_details_list = [
    #     Product.id,
    #     Product.name,
    #     Product.description,
    #     Product.price,
    #     Product.category_id,
    #     Product.image_url,
    #     Product.created_at
    # ]
    # column_searchable_list = [Product.name]

    # column_sortable_list = [
    #     Product.id,
    #     Product.price,
    #     Product.created_at
    # ]

    # column_filters = ["user_id", "product_id", "price", "total_price", "created_at"]  # ✅ строки

    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-box"