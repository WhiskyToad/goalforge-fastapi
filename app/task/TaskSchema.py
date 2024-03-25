from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    recurring: bool
    recurring_interval: Optional[str] = None


class TaskSchema(TaskBase):
    id: int
    created_at: datetime
    owner_id: int


class EditTaskInput(TaskBase):
    task_id: int


class CreateTaskInput(TaskBase):
    due_date: str


class CreateTaskInstanceInput(BaseModel):
    task_id: int
    due_date: str


class TaskInstanceSchema(BaseModel):
    task_id: int
    title: str
    description: str
    id: int
    completed: bool
    completed_at: Optional[datetime]
    due_date: Optional[datetime]
    status: str
