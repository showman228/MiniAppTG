from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.auth.jwt import decode_access_token
from server.app.crud.user_crud import CRUDUser
from server.app.database import get_db
from server.app.models.user import User

bearer_token = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_token),
        db: AsyncSession = Depends(get_db)
) -> User:

    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = int(payload["sub"])
    user = await CRUDUser(db).get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user