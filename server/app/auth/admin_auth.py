import os
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Для начала можно сделать простую проверку (потом заменим на поиск в БД)
        if username == "admin" and password == "12345":
            request.session.update({"token": "admin_access"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True

# Секретный ключ для шифрования сессий (можно взять из вашего config.py)
authentication_backend = AdminAuth(secret_key=os.environ.get("SECRET_KEY"))