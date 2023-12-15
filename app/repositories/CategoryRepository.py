from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection


class CategoryRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_category(self, category_input, user_id):
        category = category_input.dict()
        category["owner_id"] = user_id

        return await self.db.create(category)
