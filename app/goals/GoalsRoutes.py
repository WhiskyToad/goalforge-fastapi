from typing import List
from fastapi import APIRouter, Depends, status
from app.auth.auth_utils import get_user_id_from_token
from app.goals.GoalsSchema import Goal, GoalCreate, GoalTaskUpdateSchema
from app.goals.GoalsService import GoalsService


GoalsRouter = APIRouter(prefix="/api/goals", tags=["goals"])


@GoalsRouter.get("/get/all", status_code=status.HTTP_200_OK, response_model=List[Goal])
async def get_all_user_goals(
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.get_all_user_goals(user_id)


@GoalsRouter.post(
    "/create",
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
    "/edit/{goal_id}",
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


@GoalsRouter.get(
    "/delete/{goal_id}", status_code=status.HTTP_200_OK, response_model=dict
)
async def delete_goal_by_id(
    goal_id: int,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.get_all_user_goals(user_id)


@GoalsRouter.patch(
    "/complete/{goal_id}",
    status_code=status.HTTP_200_OK,
    response_model=Goal,
)
async def complete_user_goal(
    goal_id: int,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.complete_user_goal(goal_id, user_id)


@GoalsRouter.patch(
    "/uncomplete/{goal_id}",
    status_code=status.HTTP_200_OK,
    response_model=Goal,
)
async def uncomplete_user_goal(
    goal_id: int,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.uncomplete_user_goal(goal_id, user_id)


@GoalsRouter.patch(
    "/add-task",
    status_code=status.HTTP_200_OK,
    response_model=Goal,
)
async def add_task_to_goal(
    input: GoalTaskUpdateSchema,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.add_task_to_goal(input.goal_id, input.task_id, user_id)
