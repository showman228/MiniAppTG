class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_admin]
    column_searchable_list = [User.email]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

