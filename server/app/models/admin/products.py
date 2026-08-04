from server.app.models.product import Product
from sqladmin import ModelView

class ProductsAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.name,
        Product.description,
        Product.price,
        Product.category_id,
        Product.created_at
    ]