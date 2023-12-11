from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from app.config.Database import get_db_connection
from app.schemas.TaskSchema import CreateTaskInput
from app.models.TaskModel import TaskInDb, TaskInstanceInDb
from app.schemas.TaskSchema import TaskInstance
from typing import Optional
from sqlalchemy import func
from datetime import date


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_task(
        self, task_input: CreateTaskInput, user_id: str
    ) -> TaskInstance:
        task = TaskInDb(
            title=task_input.title,
            description=task_input.description,
            recurring=task_input.recurring,
            owner_id=user_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    async def create_task_instance(
        self, task_id: int, due_date: Optional[str]
    ) -> TaskInstanceInDb:
        task_instance = TaskInstanceInDb(task_id=task_id, due_date=due_date)
        self.db.add(task_instance)
        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    def get_task_by_id_and_owner(self, task_id: int, owner_id: str):
        return (
            self.db.query(TaskInDb)
            .filter(TaskInDb.id == task_id, TaskInDb.owner_id == owner_id)
            .first()
        )

    async def get_tasks_by_due_date(self, due_date: date, user_id: str):
        tasks = (
            self.db.query(TaskInDb, TaskInstanceInDb)
            .join(TaskInstanceInDb, TaskInDb.id == TaskInstanceInDb.task_id)
            .filter(
                TaskInDb.owner_id == user_id,
                func.date(TaskInstanceInDb.due_date) == due_date,
            )
            .all()
        )
        return tasks
