from server.app.models.product import Product
from sqladmin import ModelView

# 3. Описываем таблицу Товаров
class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.description, Product.category_id, Product.created_at]
    column_filters = [Product.price, Product.name, Product.created_at, Product.category_id]
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-box"