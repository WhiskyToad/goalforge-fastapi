from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.schemas.TaskSchema import CreateTaskInput
from app.models.TaskModel import TaskInDb, TaskInstanceInDb


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create_task(self, task_input: CreateTaskInput, user_id: str):
        task = TaskInDb(**task_input.dict(), owner_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        task_instance = self.create_task_instance(task.id, task_input.due_date)
        return task, task_instance

    def create_task_instance(self, task_id: int, due_date: str | None):
        task_instance = TaskInstanceInDb(task_id=task_id, due_date=due_date)
        self.db.add(task_instance)
        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance
