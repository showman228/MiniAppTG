import os
import secrets

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from server.app.config import settings


ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username") or ""
        password = form.get("password") or ""

        if not ADMIN_PASSWORD:
            return False

        ok_user = secrets.compare_digest(username, ADMIN_USERNAME)
        ok_pass = secrets.compare_digest(password, ADMIN_PASSWORD)
        if ok_user and ok_pass:
            request.session.update({"token": "admin_access"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("token"))


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
