from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from app.config.Database import get_db_connection
from app.schemas.TaskSchema import CreateTaskInput
from app.models.TaskModel import Task, TaskInstance
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
        task = Task(
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
    ) -> TaskInstance:
        task_instance = TaskInstance(task_id=task_id, due_date=due_date)
        self.db.add(task_instance)
        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    def get_task_by_id_and_owner(self, task_id: int, owner_id: str):
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.owner_id == owner_id)
            .first()
        )

    async def get_tasks_by_due_date(self, due_date: date, user_id: str):
        tasks = (
            self.db.query(Task, TaskInstance)
            .join(TaskInstance, Task.id == TaskInstance.task_id)
            .filter(
                Task.owner_id == user_id,
                func.date(TaskInstance.due_date) == due_date,
            )
            .all()
        )
        return tasks
