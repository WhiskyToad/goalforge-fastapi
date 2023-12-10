from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.schemas.TaskSchema import CreateTaskInput
from app.models.TaskModel import TaskInDb, TaskInstanceInDb
from app.schemas.TaskSchema import TaskInstance
from typing import Optional


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
        task_instance = await self.create_task_instance(task.id, task_input.due_date)
        return TaskInstance(
            task_id=task.id,
            title=task.title,
            description=task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at,
            due_date=task_instance.due_date,
            status=task_instance.status,
        )

    async def create_task_instance(
        self, task_id: int, due_date: Optional[str]
    ) -> TaskInstanceInDb:
        task_instance = TaskInstanceInDb(task_id=task_id, due_date=due_date)
        self.db.add(task_instance)
        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance
