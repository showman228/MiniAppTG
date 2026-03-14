from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    telegram_id: int  # это число, не строка
    username: Optional[str] = None
    firstname: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int = Field(..., description="User ID")

    class Config:
        from_attributes = True
