from fastapi import Depends

from app.goals.GoalsRepository import GoalsRepository
from app.goals.GoalsSchema import Goal, GoalCreate


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
