from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.core.auth import get_current_user
from server.app.database import get_db
from server.app.models.user import User
from server.app.schemas.user import UserCreate, UserResponse
from server.app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user_data)


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/all_users", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    services = UserService(db)
    return await services.get_all_users()
