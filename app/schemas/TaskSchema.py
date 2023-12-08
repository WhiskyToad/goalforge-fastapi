from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateTaskInput(BaseModel):
    title: str
    description: str
    recurring: bool
    due_date: Optional[datetime] = None
