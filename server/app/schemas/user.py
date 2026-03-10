from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=30, description="@username")
    email: EmailStr = Field(..., description="email address by user")

class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., min_length=5, max_length=30, description="@username")
    email: EmailStr = Field(..., description="email address by user")

    class Config:
        from_attributes = True
