from typing import List
from fastapi import Depends, status
from app.task.TaskRepository import TaskRepository
from app.task.TaskSchema import (
    CompleteTaskInstanceInput,
    CreateTaskInput,
    TaskInstanceSchema,
    CreateTaskInstanceInput,
    EditTaskInput,
    TaskSchema,
)
from app.task.TaskModel import Task
from app.shared.errors.CustomError import CustomError
from datetime import date, datetime

from app.task.TaskUtils import map_task_task_instances, map_task_to_schema

TASK_NOT_FOUND = "Task not found"


class TaskService:
    task_repository: TaskRepository

    def __init__(
        self,
        task_repository: TaskRepository = Depends(TaskRepository),
    ) -> None:
        self.task_repository = task_repository

    async def get_task_by_id(self, task_id: int, user_id: int) -> TaskSchema:
        task, instances = await self.task_repository.get_task_by_id_and_owner(
            task_id, user_id
        )
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        return map_task_to_schema(task, instances)

    async def get_all_tasks(self, user_id: int) -> list[TaskSchema]:
        task_tuples = await self.task_repository.get_all_tasks_for_owner(user_id)

        return [
            map_task_to_schema(task, task_instances)
            for task, task_instances in task_tuples
            if task is not None
        ]

    async def create_task(
        self,
        task_input: CreateTaskInput,
        user_id: int,
    ) -> TaskInstanceSchema:
        task = Task(
            title=task_input.title,
            description=task_input.description,
            recurring=task_input.recurring,
            owner_id=user_id,
            is_habit=task_input.is_habit,
            icon=task_input.icon,
        )
        task_in_db = await self.task_repository.create_task(task)
        task_instance = await self.task_repository.create_task_instance(
            task.id, datetime.fromisoformat(task_input.due_date)
        )
        return map_task_task_instances(task_in_db, task_instance)

    async def create_task_instance(
        self,
        task_input: CreateTaskInstanceInput,
        user_id: int,
    ) -> TaskInstanceSchema:
        task_tuple = await self.task_repository.get_task_by_id_and_owner(
            task_input.task_id, user_id
        )
        task, _ = task_tuple
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        task_instance = await self.task_repository.create_task_instance(
            task_input.task_id, datetime.fromisoformat(task_input.due_date)
        )
        return map_task_task_instances(task, task_instance)

    async def get_tasks_by_due_date(self, due_date: date, user_id: int):
        task_instances = await self.task_repository.get_tasks_by_due_date(
            due_date, user_id
        )
        return [
            map_task_task_instances(task, task_instance)
            for task, task_instance in task_instances
        ]

    async def complete_task_instance(
        self, input: CompleteTaskInstanceInput, task_instance_id: int, user_id: int
    ):
        task_instance = await self.task_repository.complete_task_instance(
            input, task_instance_id, user_id
        )
        if task_instance is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )

        return TaskInstanceSchema(
            task_id=task_instance.task.id,
            task_title=task_instance.task.title,
            description=task_instance.task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at.isoformat(),
            due_date=task_instance.due_date.isoformat(),
            status=task_instance.status,
            task_icon=task_instance.task.icon,
        )

    async def uncomplete_task_instance(self, task_instance_id: int, user_id: int):
        task_instance = await self.task_repository.uncomplete_task_instance(
            task_instance_id, user_id
        )
        if task_instance is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )

        return TaskInstanceSchema(
            task_id=task_instance.task.id,
            task_title=task_instance.task.title,
            task_icon=task_instance.task.icon,
            description=task_instance.task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at,
            due_date=task_instance.due_date,
            status=task_instance.status,
        )

    async def edit_task(self, task_id: int, task_input: EditTaskInput, user_id: int):
        task = await self.task_repository.edit_task(task_id, task_input, user_id)
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        return map_task_to_schema(task, [])

    def delete_task_instance(self, instance_id: int, user_id: int):
        return self.task_repository.delete_task_instance(instance_id, user_id)

    async def get_tasks_by_ids(
        self, task_ids: List[int], user_id: int
    ) -> List[TaskSchema]:
        task_tuples = await self.task_repository.get_tasks_by_ids_and_user_id(
            task_ids, user_id
        )
        return [
            map_task_to_schema(task, task_instances)
            for task, task_instances in task_tuples
            if task is not None
        ]
