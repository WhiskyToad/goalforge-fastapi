from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.BaseModel import EntityMeta


class Task(EntityMeta):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    recurring = Column(Boolean, default=False)
    recurring_interval = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="tasks")

    category_id = Column(Integer, ForeignKey("task_categories.id"))
    category = relationship("TaskCategory", back_populates="tasks")

    task_instances = relationship("TaskInstance", back_populates="task")


class TaskInstance(EntityMeta):
    __tablename__ = "task_instances"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True, default=None)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    due_date = Column(DateTime)
    status = Column(String, default="pending")

    task = relationship("Task", back_populates="task_instances")


class TaskCategory(EntityMeta):
    __tablename__ = "task_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
