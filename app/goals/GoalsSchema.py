from pydantic import BaseModel
from typing import List, Optional


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[str]


class Goal(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    target_date: Optional[str]
    task_ids: List[str]


class GoalTaskUpdateSchema(BaseModel):
    goal_id: int
    task_id: int
