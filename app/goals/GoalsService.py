from fastapi import Depends

from app.goals.GoalsRepository import GoalsRepository


class GoalsService:
    goals_repository: GoalsRepository

    def __init__(
        self,
        goals_repository: GoalsRepository = Depends(GoalsRepository),
    ) -> None:
        self.goals_repository = goals_repository  # Placeholder file
