from server.app.models.user import User
from server.app.schemas.user import UserCreate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List


class CRUDUser:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[User]:
        users = await self.db.execute(select(User))
        return list(users.scalars().all())

    async def get_by_id(self, user_id: int) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.email == email))
        return user.scalars().one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalars().one_or_none()

    async def create(self, user_data: UserCreate, password_hash: str) -> User:
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            username=user_data.username,
            firstname=user_data.firstname
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserCreate) -> Optional[User]:
        user = await self.get_by_id(user_id)

        if user is None:
            return None

        for field, value in user_data.model_dump(exclude_unset=True, exclude={"password"}).items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)

        if user is None:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True
