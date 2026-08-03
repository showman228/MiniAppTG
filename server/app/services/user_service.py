from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from server.app.crud.user_crud import CRUDUser
from server.app.core.security import hash_password, verify_password
from server.app.models.user import User
from server.app.schemas.user import UserCreate, UserResponse


class UserService:

    def __init__(self, db: AsyncSession):
        self.user_crud = CRUDUser(db)

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.user_crud.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found by user_id")
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.user_crud.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found by email")
        return UserResponse.model_validate(user)

    async def get_user_by_username(self, username: str) -> UserResponse:
        user = await self.user_crud.get_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found by username")
        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing = await self.user_crud.get_by_email(user_data.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        password_hash = hash_password(user_data.password)
        user = await self.user_crud.create(user_data, password_hash)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: UserCreate) -> UserResponse:
        user = await self.user_crud.update(user_id, user_data)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found by user_id")
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.user_crud.delete(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found by user_id")
        return True

    async def authenticate(self, username: str, password: str) -> User:
        unauthed_exc_username = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email",
            headers={"WWW-Authenticate": "Basic"}
        )

        unauthed_exc_password = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Basic"}
        )

        user = await self.user_crud.get_by_username(username)
        if user is None:
            raise unauthed_exc_username

        if not verify_password(password, user.password_hash):
            raise unauthed_exc_password

        return user
