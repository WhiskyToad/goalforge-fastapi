from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.categories.CategoryModel import TaskCategory
from app.categories.CategorySchema import CreateCategoryInput


class CategoryRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_category(self, category_input: CreateCategoryInput, user_id: int):
        category = TaskCategory(
            name=category_input.name,
            description=category_input.description,
            owner_id=user_id,
        )

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    async def delete_category(self, category_id: int, user_id: int):
        category = (
            self.db.query(TaskCategory)
            .filter(TaskCategory.id == category_id, TaskCategory.owner_id == user_id)
            .first()
        )
        self.db.delete(category)
        self.db.commit()
        return {"success": True}

    async def edit_category(
        self, category_id: int, category_input: CreateCategoryInput, user_id: int
    ):
        category = (
            self.db.query(TaskCategory)
            .filter(TaskCategory.id == category_id, TaskCategory.owner_id == user_id)
            .first()
        )
        if not category:
            return None
        category.name = category_input.name
        category.description = category_input.description
        self.db.commit()
        self.db.refresh(category)
        return category

    async def get_all_categories(self, user_id: int):
        categories = (
            self.db.query(TaskCategory).filter(TaskCategory.owner_id == user_id).all()
        )
        return categories
