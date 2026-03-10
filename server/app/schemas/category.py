from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=25, description="Name of category")
    slug: str = Field(..., min_length=5, max_length=25, description="URl - friendly category name")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="Unique identifier for this category")

    class Config:
        from_attributes = True