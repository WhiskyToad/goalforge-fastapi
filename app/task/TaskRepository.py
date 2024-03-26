from fastapi import Depends
from sqlalchemy.orm import Session
from app.shared.config.Database import get_db_connection
from app.task.TaskSchema import EditTaskInput
from app.task.TaskModel import Task, TaskInstance
from typing import Optional
from sqlalchemy import func
from datetime import date


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    async def create_task_instance(
        self, task_id: int, due_date: Optional[date]
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

    async def complete_task_instance(self, task_instance_id: int, user_id: str):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == task_instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        if task_instance is None:
            return None

        task_instance.completed = True
        task_instance.completed_at = func.now()
        task_instance.status = "completed"

        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    async def uncomplete_task_instance(self, task_instance_id: int, user_id: str):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == task_instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        if task_instance is None:
            return None

        task_instance.completed = False
        task_instance.completed_at = None
        task_instance.status = "pending"

        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    async def edit_task(self, task_input: EditTaskInput, user_id: str):
        task = (
            self.db.query(Task)
            .filter(Task.id == task_input.task_id, Task.owner_id == user_id)
            .first()
        )
        if task is None:
            return None
        task.title = task_input.title
        task.description = task_input.description
        task.recurring = task_input.recurring
        self.db.commit()
        self.db.refresh(task)
        return task

    async def delete_task_instance(self, instance_id: int, user_id: str):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        self.db.delete(task_instance)
        self.db.commit()
        return {"success": True}
