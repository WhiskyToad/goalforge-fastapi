from typing import List
from fastapi import Depends, status
from app.task.TaskRepository import TaskRepository
from app.task.TaskSchema import (
    CreateTaskInput,
    TaskInstanceSchema,
    CreateTaskInstanceInput,
    EditTaskInput,
    TaskSchema,
)
from app.task.TaskModel import Task, TaskInstance
from app.shared.errors.CustomError import CustomError
from datetime import date, datetime

TASK_NOT_FOUND = "Task not found"


def map_task_to_schema(task: tuple[Task, list[TaskInstance]]) -> TaskSchema:
    task_obj, instances = task
    return TaskSchema(
        id=task_obj.id,
        title=task_obj.title,
        description=task_obj.description,
        recurring=task_obj.recurring,
        recurring_interval=task_obj.recurring_interval,
        created_at=task_obj.created_at.isoformat(),
        is_habit=task_obj.is_habit,
        icon=task_obj.icon,
        instances=[map_instance_to_schema(instance) for instance in instances],
    )


def map_instance_to_schema(instance: TaskInstance) -> TaskInstanceSchema:
    return TaskInstanceSchema(
        task_id=instance.task_id,
        title=instance.task.title,
        description=instance.task.description,
        id=instance.id,
        completed=instance.completed,
        completed_at=(
            instance.completed_at.isoformat() if instance.completed_at else None
        ),
        due_date=instance.due_date.isoformat() if instance.due_date else None,
        status=instance.status,
    )


class TaskService:
    task_repository: TaskRepository

    def __init__(
        self,
        task_repository: TaskRepository = Depends(TaskRepository),
    ) -> None:
        self.task_repository = task_repository

    async def get_task_by_id(self, task_id: int, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_task_by_id_and_owner(task_id, user_id)
        return map_task_to_schema(task)

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
        return self.map_task_task_instances(task_in_db, task_instance)

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
        return self.map_task_task_instances(task, task_instance)

    async def get_tasks_by_due_date(self, due_date: date, user_id: int):
        task_instances = await self.task_repository.get_tasks_by_due_date(
            due_date, user_id
        )
        return [
            self.map_task_task_instances(task, task_instance)
            for task, task_instance in task_instances
        ]

    async def complete_task_instance(self, task_instance_id: int, user_id: int):
        task_instance = await self.task_repository.complete_task_instance(
            task_instance_id, user_id
        )
        if task_instance is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )

        return TaskInstanceSchema(
            task_id=task_instance.task.id,
            title=task_instance.task.title,
            description=task_instance.task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at,
            due_date=task_instance.due_date,
            status=task_instance.status,
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
            title=task_instance.task.title,
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
        return map_task_to_schema(task)

    def map_task_task_instances(
        self, task: Task, task_instance: TaskInstance
    ) -> TaskInstanceSchema:
        due_date_str = task_instance.due_date.isoformat()
        return TaskInstanceSchema(
            task_id=task.id,
            title=task.title,
            description=task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at,
            due_date=due_date_str,
            status=task_instance.status,
        )

    def delete_task_instance(self, instance_id: int, user_id: int):
        return self.task_repository.delete_task_instance(instance_id, user_id)

    async def get_tasks_by_ids(
        self, task_ids: List[int], user_id: int
    ) -> List[TaskSchema]:
        tasks_list = await self.task_repository.get_tasks_by_ids_and_user_id(
            task_ids, user_id
        )
        return [map_task_to_schema(task) for task in tasks_list]
