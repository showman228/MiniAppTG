from fastapi import HTTPException
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

from server.app.database import SessionLocal
from server.app.services.user_service import UserService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        async with SessionLocal() as session:
            service = UserService(session)
            try:
                user = await service.authenticate(str(username), str(password))
            except HTTPException:
                return False

        if not user.is_admin:
            return False

        request.session.update({"is_admin": True, "username": user.username})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("is_admin"))
