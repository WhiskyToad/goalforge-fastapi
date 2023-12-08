from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self):
        pass
