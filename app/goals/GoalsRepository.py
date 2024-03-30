from fastapi import Depends
from sqlalchemy.orm import Session

from app.goals.GoalsModel import GoalModel
from app.goals.GoalsSchema import GoalCreate
from app.shared.config.Database import get_db_connection


class GoalsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_user_goal(self, goal_data: GoalCreate, user_id: int) -> GoalModel:
        goal = GoalModel(**goal_data, user_id=user_id)
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal
