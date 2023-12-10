from fastapi import Depends, status
from typing import Type
from app.repositories.TaskRepository import TaskRepository
from app.schemas.TaskSchema import (
    CreateTaskInput,
    TaskInstance,
    CreateTaskInstanceInput,
)
from app.errors.CustomError import CustomError


class TaskService:
    task_repository: Type[TaskRepository]

    def __init__(
        self,
        task_repository: Type[TaskRepository] = Depends(TaskRepository),
    ) -> None:
        self.task_repository = task_repository

    async def create_task(
        self,
        task_input: CreateTaskInput,
        user_id: str,
    ) -> TaskInstance:
        task_data = await self.task_repository.create_task(task_input, user_id)
        return task_data

    async def create_task_instance(
        self,
        task_input: CreateTaskInstanceInput,
        user_id: str,
    ) -> TaskInstance:
        task = self.task_repository.get_task_by_id(task_input.task_id)
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Task not found",
            )
        if user_id != task.owner_id:
            raise CustomError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Not Authorized",
            )
        task_instance = await self.task_repository.create_task_instance(
            task_input.task_id, task_input.due_date
        )
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
