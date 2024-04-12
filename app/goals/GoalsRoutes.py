from typing import List
from fastapi import APIRouter, Depends, status
from app.auth.auth_utils import get_user_id_from_token
from app.goals.GoalsSchema import Goal, GoalCreateInput, GoalTaskUpdateInput
from app.goals.GoalsService import GoalsService


GoalsRouter = APIRouter(prefix="/api/goals", tags=["goals"])


@GoalsRouter.get("/{goal_id}", status_code=status.HTTP_200_OK, response_model=Goal)
async def get_goal_by_id(
    goal_id: int,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.get_goal_by_id(goal_id, user_id)


@GoalsRouter.get("/", status_code=status.HTTP_200_OK, response_model=List[Goal])
async def get_all_user_goals(
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.get_all_user_goals(user_id)


@GoalsRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Goal,
)
async def create_user_goal(
    goal_data: GoalCreateInput,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.create_user_goal(user_id, goal_data)


@GoalsRouter.patch(
    "/{goal_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Goal,
)
async def edit_user_goal(
    goal_id: int,
    goal_data: GoalCreateInput,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.update_user_goal(goal_id, user_id, goal_data)


@GoalsRouter.patch(
    "/{goal_id}/complete",
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
    "/{goal_id}/uncomplete",
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
    "/{goal_id}/add-task",
    status_code=status.HTTP_200_OK,
    response_model=Goal,
)
async def add_task_to_goal(
    goal_id: int,
    input: GoalTaskUpdateInput,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.add_task_to_goal(goal_id, input.task_id, user_id)


@GoalsRouter.patch(
    "/{goal_id}/remove-task",
    status_code=status.HTTP_200_OK,
    response_model=Goal,
)
async def remove_task_from_goal(
    goal_id: int,
    input: GoalTaskUpdateInput,
    user_id: int = Depends(get_user_id_from_token),
    goals_service: GoalsService = Depends(GoalsService),
):
    return await goals_service.remove_task_from_goal(goal_id, input.task_id, user_id)
