from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.database import get_db
from server.app.models.user import User
from server.app.services.user_service import UserService

security = HTTPBasic()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: AsyncSession = Depends(get_db),
) -> User:
    service = UserService(db)
    return await service.authenticate(credentials.username, credentials.password)
