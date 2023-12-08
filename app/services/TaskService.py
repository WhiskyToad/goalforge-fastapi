from fastapi import Depends
from typing import Type
from app.repositories.TaskRepository import TaskRepository


class UserService:
    task_repository: Type[TaskRepository]

    def __init__(
        self,
        task_repository: Type[TaskRepository] = Depends(TaskRepository),
    ) -> None:
        self.task_repository = task_repository

    async def create_task(
        self,
    ):
        return self.task_repository.create()
