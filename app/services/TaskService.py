from fastapi import Depends
from typing import Type
from app.repositories.TaskRepository import TaskRepository
from app.schemas.TaskSchema import CreateTaskInput, TaskInstance


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
