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
    owner = relationship("UserModel", back_populates="tasks")

    def normalize(self):
        return {
            "title": self.title.__str__(),
            "description": self.description.__str__(),
        }


class TaskInstanceInDb(EntityMeta):
    __tablename__ = "task_instances"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True, default=None)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    due_date = Column(DateTime)
    status = Column(String, default="pending")
