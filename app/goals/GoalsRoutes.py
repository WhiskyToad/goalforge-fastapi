from fastapi import APIRouter, Depends, status
from app.auth.auth_utils import get_user_id_from_token


GoalsRouter = APIRouter(prefix="/api/goals", tags=["goals"])


@GoalsRouter.post(
    "/create/goal",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def create_user_goal():
    return None
