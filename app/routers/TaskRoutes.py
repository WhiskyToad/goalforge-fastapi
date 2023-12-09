from fastapi import Depends, APIRouter
from app.utils.auth import get_user_id_from_token
from app.schemas.TaskSchema import CreateTaskInput, TaskInstance
from app.services.TaskService import TaskService


TaskRouter = APIRouter(prefix="/api/task", tags=["task"])


@TaskRouter.post("/create", status_code=201, response_model=TaskInstance)
async def create(
    task_input: CreateTaskInput,
    user_id: str = Depends(get_user_id_from_token),
    task_service: TaskService = Depends(TaskService),
):
    return await task_service.create_task(task_input, user_id)
