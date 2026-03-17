from sqladmin import ModelView
from server.app.models.user import User

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id, User.username, User.firstname]
    column_searchable_list = [User.username]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"