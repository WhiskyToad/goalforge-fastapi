from fastapi import Depends, APIRouter
from app.utils.auth import get_user_id_from_token


TaskRouter = APIRouter(prefix="/api/task", tags=["task"])


@TaskRouter.post("/create", status_code=201)
async def create(
    user_id: str = Depends(get_user_id_from_token),
):
    return user_id
