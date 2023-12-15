from fastapi import Depends, status
from typing import Type
from app.repositories.CategoryRepository import CategoryRepository
from app.errors.CustomError import CustomError
from datetime import date


class CategoryService:
    category_repository: Type[CategoryRepository]

    def __init__(
        self,
        category_repository: Type[CategoryRepository] = Depends(CategoryRepository),
    ) -> None:
        self.category_repository = category_repository

    async def create_category(self, category_input, user_id):
        return await self.category_repository.create_category(
            category_input, user_id, date.today()
        )
