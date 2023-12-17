from fastapi import Depends
from typing import Type
from app.repositories.CategoryRepository import CategoryRepository
from datetime import date
from app.schemas.CategorySchema import CategorySchema, CreateCategoryInput


class CategoryService:
    category_repository: Type[CategoryRepository]

    def __init__(
        self,
        category_repository: Type[CategoryRepository] = Depends(CategoryRepository),
    ) -> None:
        self.category_repository = category_repository

    async def create_category(
        self, category_input: CreateCategoryInput, user_id: str
    ) -> CategorySchema:
        category = await self.category_repository.create_category(
            category_input, user_id
        )
        return CategorySchema(
            id=category.id, name=category.name, description=category.description
        )
