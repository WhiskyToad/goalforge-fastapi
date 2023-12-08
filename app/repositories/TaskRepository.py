from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.schemas.TaskSchema import CreateTaskInput


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, task_input: CreateTaskInput, user_id: str):
        pass
