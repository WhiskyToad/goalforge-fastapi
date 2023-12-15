from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CreateCategoryInput(CategoryBase):
    pass


class EditCategoryInput(CategoryBase):
    id: int


class CategorySchema(CategoryBase):
    id: int
