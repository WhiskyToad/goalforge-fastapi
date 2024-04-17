from typing import List, Optional

from pydantic import BaseModel


class TaskInstanceSchema(BaseModel):
    task_id: int
    title: str
    description: str
    id: int
    completed: bool
    completed_at: Optional[str]
    due_date: Optional[str]
    status: str


class TaskBase(BaseModel):
    title: str
    description: str
    recurring: bool
    recurring_interval: Optional[str] = None
    is_habit: bool
    icon: str
    instances: List[TaskInstanceSchema]


class TaskSchema(TaskBase):
    id: int
    created_at: str
    # completed_instances: int


class EditTaskInput(TaskBase):
    pass


class CreateTaskInput(TaskBase):
    due_date: str


class CreateTaskInstanceInput(BaseModel):
    task_id: int
    due_date: str
