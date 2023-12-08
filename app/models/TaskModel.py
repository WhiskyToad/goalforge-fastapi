from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.BaseModel import EntityMeta


class TaskInDb(EntityMeta):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    def normalize(self):
        return {}


class TaskInstanceInDb(EntityMeta):
    __tablename__ = "task_instances"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, default=None)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    due_date = Column(Date)
    status = Column(String, default="pending")

    def normalize(self):
        return {}
