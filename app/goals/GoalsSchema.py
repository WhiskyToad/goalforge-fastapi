from pydantic import BaseModel
from typing import Optional


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    target_date: Optional[str]


class Goal(BaseModel):
    title: str
    description: Optional[str]
    is_completed: bool
    target_date: Optional[str]
