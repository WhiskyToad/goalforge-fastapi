from fastapi import Depends, APIRouter, status
from app.auth.auth_utils import get_user_id_from_token
from app.task.TaskSchema import (
    CreateTaskInput,
    TaskInstanceSchema,
    CreateTaskInstanceInput,
    EditTaskInput,
    TaskSchema,
)
from app.shared.schemas.GenericSchema import SuccessMessage
from app.task.TaskService import TaskService
from datetime import date
from typing import List


TaskRouter = APIRouter(prefix="/api/task", tags=["task"])


@TaskRouter.post(
    "/create/task",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInstanceSchema,
)
async def create_task(
    task_input: CreateTaskInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task(task_input, user_id)


@TaskRouter.post(
    "/create/task_instance",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInstanceSchema,
)
async def create_task_instance(
    task_input: CreateTaskInstanceInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task_instance(task_input, user_id)


@TaskRouter.get(
    "/tasks/{due_date}",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskInstanceSchema],
)
async def get_tasks_by_due_date(
    due_date: date = date.today(),
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.get_tasks_by_due_date(due_date, user_id)


@TaskRouter.patch(
    "/complete/{task_instance_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskInstanceSchema,
)
async def complete_task_instance(
    task_instance_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.complete_task_instance(task_instance_id, user_id)


@TaskRouter.patch(
    "/uncomplete/{task_instance_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskInstanceSchema,
)
async def uncomplete_task_instance(
    task_instance_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.uncomplete_task_instance(task_instance_id, user_id)


@TaskRouter.patch(
    "/edit/{task__id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskSchema,
)
async def edit_task(
    task_input: EditTaskInput,
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.edit_task(task_input, user_id)


@TaskRouter.delete(
    "/delete/instance/{instance_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_task_instance(
    instance_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.delete_task_instance(instance_id, user_id)
