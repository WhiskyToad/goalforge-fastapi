from pydantic import BaseModel
from typing import List, Optional

from app.task.TaskSchema import TaskSchema


class GoalCreateInput(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[str]
    icon: str


class Goal(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    target_date: Optional[str]
    tasks: List[TaskSchema]
    icon: str


class GoalTaskUpdateInput(BaseModel):
    task_id: int
