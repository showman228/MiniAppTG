from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.auth.telegram import verify_telegram_init_data
from server.app.auth.jwt import create_access_token
from server.app.crud.user_crud import CRUDUser
from server.app.schemas.user import UserCreate
from server.app.database import get_db

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)

class AuthRequest(BaseModel):
    init_data: str  # строка от window.Telegram.WebApp.initData

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int


@router.post('/verify', response_model=AuthResponse)
async def verify_auth(
        body: AuthRequest,
        db: AsyncSession = Depends(get_db)
):
    tg_user = verify_telegram_init_data(body.init_data)

    telegram_id = tg_user.get('id')
    if not telegram_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No user id in initData")

    crud = CRUDUser(db)
    user = await crud.get_by_telegram_id(telegram_id)

    if user is None:
        user = await crud.create(UserCreate(
            telegram_id=telegram_id,
            firstname=tg_user.get('firstname'),
            username=tg_user.get('username')
        ))

    token = create_access_token(user_id=user.id, telegram_id=telegram_id)
    return AuthResponse(access_token=token, user_id=user.id, token_type="bearer")