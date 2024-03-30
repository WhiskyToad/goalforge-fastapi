from fastapi import Depends, status

from app.goals.GoalsRepository import GoalsRepository
from app.goals.GoalsSchema import Goal, GoalCreate
from app.shared.errors.CustomError import CustomError


GOAL_NOT_FOUND = "Goal not found"


class GoalsService:
    goals_repository: GoalsRepository

    def __init__(
        self,
        goals_repository: GoalsRepository = Depends(GoalsRepository),
    ) -> None:
        self.goals_repository = goals_repository

    async def create_user_goal(self, user_id: int, goal_data: GoalCreate) -> Goal:
        goal = await self.goals_repository.create_user_goal(goal_data, user_id)
        return Goal(
            title=goal.title,
            description=goal.description,
            is_completed=False,
            target_date=goal.target_date,
        )

    async def update_user_goal(
        self, goal_id: int, user_id: int, goal_data: GoalCreate
    ) -> Goal:
        goal = await self.goals_repository.update_user_goal(goal_id, user_id, goal_data)
        if not goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        return Goal(
            title=goal.title,
            description=goal.description,
            is_completed=goal.is_completed,
            target_date=goal.target_date,
        )
