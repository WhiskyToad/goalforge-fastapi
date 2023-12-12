from fastapi import Depends, APIRouter
from app.utils.auth import get_user_id_from_token
from app.schemas.TaskSchema import (
    CreateTaskInput,
    TaskInstanceSchema,
    CreateTaskInstanceInput,
)
from app.services.TaskService import TaskService
from datetime import date
from typing import List


TaskRouter = APIRouter(prefix="/api/task", tags=["task"])


@TaskRouter.post("/create/task", status_code=201, response_model=TaskInstanceSchema)
async def create_task(
    task_input: CreateTaskInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task(task_input, user_id)


@TaskRouter.post(
    "/create/task_instance", status_code=201, response_model=TaskInstanceSchema
)
async def create_task_instance(
    task_input: CreateTaskInstanceInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task_instance(task_input, user_id)


@TaskRouter.get("/tasks/{due_date}", response_model=List[TaskInstanceSchema])
async def get_tasks_by_due_date(
    due_date: date,
    task_service: TaskService = Depends(TaskService),
    user_id: str = Depends(get_user_id_from_token),
):
    return await task_service.get_tasks_by_due_date(due_date, user_id)
