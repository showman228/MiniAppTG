from sqladmin import ModelView
from server.app.models.category import Category

class CategoriesAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.name,
        Category.slug
    ]