from typing import List
from fastapi import Depends, status

from app.goals.GoalsModel import GoalModel
from app.goals.GoalsRepository import GoalsRepository
from app.goals.GoalsSchema import Goal, GoalCreateInput
from app.shared.errors.CustomError import CustomError
from app.task.TaskRepository import TaskRepository
from app.task.TaskService import TASK_NOT_FOUND


GOAL_NOT_FOUND = "Goal not found"


async def map_goal_model_to_goal(goal_model: GoalModel) -> Goal:
    return Goal(
        id=goal_model.id,
        title=goal_model.title,
        description=goal_model.description,
        is_completed=goal_model.is_completed,
        target_date=goal_model.target_date,
        task_ids=[task.id for task in goal_model.tasks],
        icon=goal_model.icon,
    )


class GoalsService:
    goals_repository: GoalsRepository
    task_repository: TaskRepository

    def __init__(
        self,
        goals_repository: GoalsRepository = Depends(GoalsRepository),
        task_repository: TaskRepository = Depends(TaskRepository),
    ) -> None:
        self.goals_repository = goals_repository
        self.task_repository = task_repository

    async def get_all_user_goals(self, user_id: int) -> List[Goal]:
        goals = await self.goals_repository.get_all_tasks_by_user_id(user_id)
        return [await map_goal_model_to_goal(goal) for goal in goals]

    async def create_user_goal(self, user_id: int, goal_data: GoalCreateInput) -> Goal:
        goal = await self.goals_repository.create_user_goal(goal_data, user_id)
        return await map_goal_model_to_goal(goal)

    async def update_user_goal(
        self, goal_id: int, user_id: int, goal_data: GoalCreateInput
    ) -> Goal:
        goal = await self.goals_repository.update_user_goal(goal_id, user_id, goal_data)
        if not goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        return await map_goal_model_to_goal(goal)

    async def complete_user_goal(self, goal_id: int, user_id: int) -> Goal:
        goal = await self.goals_repository.complete_goal(goal_id, user_id)
        if not goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        return await map_goal_model_to_goal(goal)

    async def uncomplete_user_goal(self, goal_id: int, user_id: int) -> Goal:
        goal = await self.goals_repository.uncomplete_goal(goal_id, user_id)
        if not goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        return await map_goal_model_to_goal(goal)

    async def add_task_to_goal(self, goal_id: int, task_id: int, user_id: int) -> Goal:
        task_tuple = await self.task_repository.get_task_by_id_and_owner(
            task_id, user_id
        )
        goal = await self.goals_repository.get_goal_by_id_and_user_id(goal_id, user_id)
        task, _ = task_tuple
        if not task:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=TASK_NOT_FOUND,
            )
        if not goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        appended_goal = await self.goals_repository.add_task_to_goal(task, goal)
        return await map_goal_model_to_goal(appended_goal)

    async def remove_task_from_goal(
        self, goal_id: int, task_id: int, user_id: int
    ) -> Goal:
        updated_goal = await self.goals_repository.remove_task_from_goal(
            task_id, goal_id, user_id
        )
        if not updated_goal:
            raise CustomError(
                status_code=status.HTTP_404_NOT_FOUND,
                message=GOAL_NOT_FOUND,
            )
        return await map_goal_model_to_goal(updated_goal)

    async def get_goal_by_id(self, goal_id: int, user_id: int) -> Goal:
        goal_model = await self.goals_repository.get_goal_by_id_and_user_id(
            goal_id, user_id
        )

        return await map_goal_model_to_goal(goal_model)
