from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.goals.GoalsModel import GoalModel, GoalTask
from app.goals.GoalsSchema import GoalCreateInput
from app.shared.config.Database import get_db_connection
from app.task.TaskModel import Task
from app.user.UserModel import UserModel


class GoalsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def get_all_tasks_by_user_id(self, user_id: int) -> List[GoalModel]:
        goals = (
            self.db.query(GoalModel)
            .join(UserModel)
            .filter(UserModel.id == user_id)
            .all()
        )
        return goals

    async def get_goal_by_id_and_user_id(
        self, goal_id: int, user_id: int
    ) -> GoalModel | None:
        goal = (
            self.db.query(GoalModel)
            .join(UserModel)
            .filter(UserModel.id == user_id, GoalModel.id == goal_id)
            .first()
        )

        return goal

    async def create_user_goal(
        self, goal_data: GoalCreateInput, user_id: int
    ) -> GoalModel:
        goal_data_dict = goal_data.dict()
        goal = GoalModel(**goal_data_dict, user_id=user_id)
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    async def update_user_goal(
        self, goal_id: int, user_id: int, goal_data: GoalCreateInput
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

    async def remove_task_from_goal(
        self, task_id: int, goal_id: int, user_id: int
    ) -> GoalModel | None:
        # Find the goal_task record associated with the task and goal
        goal_task = (
            self.db.query(GoalTask)
            .filter(
                GoalTask.goal_id == goal_id,
                GoalTask.task_id == task_id,
            )
            .first()
        )

        # Check if the goal_task exists
        if not goal_task:
            return None  # The task is not associated with the goal

        try:
            # Remove the task from the goal's list of tasks
            goal = (
                self.db.query(GoalModel)
                .filter(GoalModel.id == goal_id, GoalModel.user_id == user_id)
                .first()
            )

            if goal:
                task_to_remove = self.db.query(Task).filter(Task.id == task_id).first()
                if task_to_remove:
                    goal.tasks.remove(task_to_remove)

            # Delete the goal_task record from the database
            self.db.delete(goal_task)
            self.db.commit()
            self.db.refresh(goal)
            return goal
        except Exception as e:
            # Handle any exceptions, such as database errors
            print(f"Error removing task from goal: {e}")
            self.db.rollback()
            return None

    async def remove_deleted_task_from_goal(self, task_id: int) -> None:
        goals = (
            self.db.query(GoalModel)
            .filter(GoalModel.tasks.any(Task.id == task_id))
            .all()
        )
        # Remove the task from each goal
        for goal in goals:
            goal.tasks = [task for task in goal.tasks if task.id != task_id]
            # Commit the changes
        self.db.commit()
