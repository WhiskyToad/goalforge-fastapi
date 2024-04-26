from datetime import datetime
from fastapi import Depends, APIRouter, Query, status
from app.auth.auth_utils import get_user_id_from_token
from app.task.TaskSchema import (
    CompleteTaskInstanceInput,
    CreateTaskInput,
    TaskInstanceSchema,
    CreateTaskInstanceInput,
    EditTaskInput,
    TaskSchema,
)
from app.shared.schemas.GenericSchema import SuccessMessage
from app.task.TaskService import TaskService
from typing import List


TaskRouter = APIRouter(prefix="/api/tasks", tags=["tasks"])


@TaskRouter.get(
    "/by-id/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskSchema,
)
async def get_task_by_id(
    task_id: str,
    user_id: int = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.get_task_by_id(int(task_id), user_id)


@TaskRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskSchema],
)
async def get_all_tasks(
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.get_all_tasks(user_id)


@TaskRouter.get(
    "/by-ids",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskSchema],
)
async def get_tasks_by_ids(
    task_ids: str = Query(..., description="List of task IDs to fetch"),
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    task_ids_list = task_ids.split(",")
    task_ids_int = [int(task_id) for task_id in task_ids_list]
    return await task_service.get_tasks_by_ids(task_ids_int, user_id)


@TaskRouter.get(
    "/due-date/{due_date}",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskInstanceSchema],
)
async def get_tasks_by_due_date(
    due_date: str,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.get_tasks_by_due_date(
        datetime.fromisoformat(due_date), user_id
    )


@TaskRouter.get(
    "/pending",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskInstanceSchema],
)
async def get_pending_tasks(
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.get_pending_tasks(user_id)


@TaskRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInstanceSchema,
)
async def create_task(
    task_input: CreateTaskInput,
    user_id: int = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task(task_input, user_id)


@TaskRouter.post(
    "/instances",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInstanceSchema,
)
async def create_task_instance(
    task_input: CreateTaskInstanceInput,
    user_id: int = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task_instance(task_input, user_id)


@TaskRouter.patch(
    "/{task_instance_id}/complete",
    status_code=status.HTTP_200_OK,
    response_model=TaskInstanceSchema,
)
async def complete_task_instance(
    task_instance_id: int,
    input: CompleteTaskInstanceInput,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.complete_task_instance(input, task_instance_id, user_id)


@TaskRouter.patch(
    "/{task_instance_id}/uncomplete",
    status_code=status.HTTP_200_OK,
    response_model=TaskInstanceSchema,
)
async def uncomplete_task_instance(
    task_instance_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.uncomplete_task_instance(task_instance_id, user_id)


@TaskRouter.patch(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskSchema,
)
async def edit_task(
    task_id: int,
    task_input: EditTaskInput,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.edit_task(task_id, task_input, user_id)


@TaskRouter.delete(
    "/instances/{instance_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_task_instance(
    instance_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.delete_task_instance(instance_id, user_id)


@TaskRouter.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(TaskService),
    user_id: int = Depends(get_user_id_from_token),
):
    return await task_service.delete_task_and_instances_by_id(task_id, user_id)
