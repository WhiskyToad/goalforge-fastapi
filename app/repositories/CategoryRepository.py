from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.models.CategoryModel import TaskCategory
from app.schemas.CategorySchema import CreateCategoryInput


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
