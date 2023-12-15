from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.models.CategoryModel import TaskCategory


class CategoryRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_category(self, category_input, user_id) -> TaskCategory:
        category = TaskCategory(
            title=category_input.title,
            description=category_input.description,
            owner_id=user_id,
        )

        self.db.create(category)
        self.db.commit()
        self.db.refresh(category)
        return category
