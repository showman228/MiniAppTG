from sqladmin import ModelView
from server.app.models.user import User

class UsersAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.firstname,
        User.username,
        User.is_admin,
    ]