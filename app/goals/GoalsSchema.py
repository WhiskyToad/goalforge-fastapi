from pydantic import BaseModel
from typing import List, Optional


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
    task_ids: List[str]
    icon: str


class GoalTaskUpdateInput(BaseModel):
    task_id: int
