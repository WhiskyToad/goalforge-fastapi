from typing import List
from fastapi import APIRouter, Depends, status
from app.auth.auth_utils import get_user_id_from_token
from app.goals.GoalsSchema import Goal, GoalCreate
from app.goals.GoalsService import GoalsService


GoalsRouter = APIRouter(prefix="/api/goals", tags=["goals"])


@GoalsRouter.get("/get/all", status_code=status.HTTP_200_OK, response_model=List[Goal])
async def get_all_user_goals(
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.get_all_user_goals(user_id)


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


@GoalsRouter.patch(
    "/edit/goal/{goal_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Goal,
)
async def edit_user_goal(
    goal_id: int,
    goal_data: GoalCreate,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.update_user_goal(goal_id, user_id, goal_data)
