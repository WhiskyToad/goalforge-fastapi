from typing import List, Optional

from pydantic import BaseModel


from enum import Enum


class TaskInstanceStatus(Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class TaskInstanceSchema(BaseModel):
    task_id: int
    task_title: str
    task_icon: str
    description: str
    id: int
    completed: bool
    completed_at: Optional[str]
    due_date: Optional[str]
    status: TaskInstanceStatus


class TaskBase(BaseModel):
    title: str
    description: str
    recurring: bool
    recurring_interval: Optional[str] = None
    is_habit: bool
    icon: str


class TaskSchema(TaskBase):
    id: int
    created_at: str
    instances: List[TaskInstanceSchema]


class EditTaskInput(TaskBase):
    pass


class CreateTaskInput(TaskBase):
    due_date: str


class CreateTaskInstanceInput(BaseModel):
    task_id: int
    due_date: str


class CompleteTaskInstanceInput(BaseModel):
    status: TaskInstanceStatus
