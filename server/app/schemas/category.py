from pydantic import BaseModel, Field
import re

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Name of category")
    slug: str = Field(..., pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

class CategoryResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for this category")
    name: str
    slug: str

    class Config:
        from_attributes = True