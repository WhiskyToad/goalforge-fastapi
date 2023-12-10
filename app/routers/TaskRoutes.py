from fastapi import Depends, APIRouter
from app.utils.auth import get_user_id_from_token
from app.schemas.TaskSchema import (
    CreateTaskInput,
    TaskInstance,
    CreateTaskInstanceInput,
)
from app.services.TaskService import TaskService


TaskRouter = APIRouter(prefix="/api/task", tags=["task"])


@TaskRouter.post("/create/task", status_code=201, response_model=TaskInstance)
async def create_task(
    task_input: CreateTaskInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task(task_input, user_id)


@TaskRouter.post("/create/task_instance", status_code=201, response_model=TaskInstance)
async def create_task_instance(
    task_input: CreateTaskInstanceInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task_instance(task_input, user_id)
