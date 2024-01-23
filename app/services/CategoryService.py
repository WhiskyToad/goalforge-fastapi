from fastapi import Depends, status
from typing import Type
from app.repositories.CategoryRepository import CategoryRepository
from app.errors.CustomError import CustomError
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

    async def delete_category(self, category_id: int, user_id: str):
        return await self.category_repository.delete_category(category_id, user_id)

    async def edit_category(
        self, category_id: int, category_input: CreateCategoryInput, user_id: str
    ) -> CategorySchema:
        category = await self.category_repository.edit_category(
            category_id, category_input, user_id
        )
        if not category:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Category not found",
            )
        return CategorySchema(
            id=category.id, name=category.name, description=category.description
        )
