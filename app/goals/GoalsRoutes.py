from fastapi import APIRouter, Depends, status
from app.auth.auth_utils import get_user_id_from_token
from app.goals.GoalsSchema import Goal, GoalCreate
from app.goals.GoalsService import GoalsService


GoalsRouter = APIRouter(prefix="/api/goals", tags=["goals"])


@GoalsRouter.post(
    "/create/goal",
    status_code=status.HTTP_201_CREATED,
    response_model=Goal,
)
async def create_user_goal(
    goal_data: GoalCreate,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.create_user_goal(user_id, goal_data)
