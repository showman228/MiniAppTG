from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    firstname: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Пароль в открытом виде, только на вход")

class UserResponse(UserBase):
    id: int = Field(..., description="User ID")

    class Config:
        from_attributes = True
