from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class CreateTaskInput(BaseModel):
    title: str
    description: str
    recurring: bool
    due_date: datetime


class CreateTaskInstanceInput(BaseModel):
    task_id: int
    due_date: datetime


class TaskInstanceSchema(BaseModel):
    task_id: int
    title: str
    description: str
    id: int
    completed: bool
    completed_at: Optional[datetime]
    due_date: Optional[datetime]
    status: str
