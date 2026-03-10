from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=30, description="@username")
    email: EmailStr = Field(..., description="email address by user")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int = Field(..., description="User ID")

    class Config:
        from_attributes = True
