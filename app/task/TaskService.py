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


class TaskService:
    task_repository: TaskRepository

    def __init__(
        self,
        task_repository: TaskRepository = Depends(TaskRepository),
    ) -> None:
        self.task_repository = task_repository

    async def create_task(
        self,
        task_input: CreateTaskInput,
        user_id: str,
    ) -> TaskInstanceSchema:
        task = Task(
            title=task_input.title,
            description=task_input.description,
            recurring=task_input.recurring,
            owner_id=user_id,
        )
        task_in_db = await self.task_repository.create_task(task)
        task_instance = await self.task_repository.create_task_instance(
            task.id, datetime.fromisoformat(task_input.due_date)
        )
        return self.map_task_task_instances(task_in_db, task_instance)

    async def create_task_instance(
        self,
        task_input: CreateTaskInstanceInput,
        user_id: str,
    ) -> TaskInstanceSchema:
        task = self.task_repository.get_task_by_id_and_owner(
            task_input.task_id, user_id
        )
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        task_instance = await self.task_repository.create_task_instance(
            task_input.task_id, datetime.fromisoformat(task_input.due_date)
        )
        return self.map_task_task_instances(task, task_instance)

    async def get_tasks_by_due_date(self, due_date: date, user_id: str):
        task_instances = await self.task_repository.get_tasks_by_due_date(
            due_date, user_id
        )
        return [
            self.map_task_task_instances(task, task_instance)
            for task, task_instance in task_instances
        ]

    async def complete_task_instance(self, task_instance_id: int, user_id: str):
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

    async def uncomplete_task_instance(self, task_instance_id: int, user_id: str):
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

    async def edit_task(self, task_input: EditTaskInput, user_id: str):
        task = await self.task_repository.edit_task(task_input, user_id)
        if task is None:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        return TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            recurring=task.recurring,
            recurring_interval=task.recurring_interval,
            created_at=task.created_at,
            owner_id=task.owner_id,
        )

    def map_task_task_instances(
        self, task: Task, task_instance: TaskInstance
    ) -> TaskInstanceSchema:
        return TaskInstanceSchema(
            task_id=task.id,
            title=task.title,
            description=task.description,
            id=task_instance.id,
            completed=task_instance.completed,
            completed_at=task_instance.completed_at,
            due_date=task_instance.due_date,
            status=task_instance.status,
        )

    def delete_task_instance(self, instance_id: int, user_id: str):
        return self.task_repository.delete_task_instance(instance_id, user_id)

    async def get_tasks_by_category(self, category_id: int, user_id: str):
        tasks = await self.task_repository.get_tasks_by_category(category_id, user_id)
        return [
            TaskSchema(
                id=task.id,
                title=task.title,
                description=task.description,
                recurring=task.recurring,
                recurring_interval=task.recurring_interval,
                created_at=task.created_at,
                owner_id=task.owner_id,
            )
            for task in tasks
        ]
