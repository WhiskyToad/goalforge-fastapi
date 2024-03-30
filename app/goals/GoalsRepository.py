from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.goals.GoalsModel import GoalModel
from app.goals.GoalsSchema import GoalCreate
from app.shared.config.Database import get_db_connection
from app.task.TaskModel import Task


class GoalsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def get_all_tasks_by_user_id(self, user_id: int) -> List[GoalModel]:
        goals = self.db.query(GoalModel).filter(GoalModel.owner == user_id).all()
        return goals

    async def get_goal_by_id_and_user_id(
        self, goal_id: int, user_id: int
    ) -> GoalModel | None:
        goal = (
            self.db.query(GoalModel)
            .filter(GoalModel.owner == user_id, GoalModel.id == goal_id)
            .first()
        )

        return goal

    async def create_user_goal(self, goal_data: GoalCreate, user_id: int) -> GoalModel:
        goal_data_dict = goal_data.dict()
        goal = GoalModel(**goal_data_dict, user_id=user_id)
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    async def update_user_goal(
        self, goal_id: int, user_id: int, goal_data: GoalCreate
    ) -> GoalModel | None:
        goal = await self.get_goal_by_id_and_user_id(goal_id, user_id)
        if not goal:
            return None

        for field, value in goal_data.dict().items():
            setattr(goal, field, value)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    async def complete_goal(self, goal_id: int, user_id: int) -> GoalModel | None:
        goal = await self.get_goal_by_id_and_user_id(goal_id, user_id)
        if not goal:
            return None
        goal.is_completed = True
        self.db.commit()
        self.db.refresh(goal)
        return goal

    async def uncomplete_goal(self, goal_id: int, user_id: int) -> GoalModel | None:
        goal = await self.get_goal_by_id_and_user_id(goal_id, user_id)
        if not goal:
            return None
        goal.is_completed = False
        self.db.commit()
        self.db.refresh(goal)
        return goal

    async def add_task_to_goal(self, task: Task, goal: GoalModel) -> GoalModel:
        goal.tasks.append(task)
        self.db.commit()
        self.db.refresh(goal)
        return goal
