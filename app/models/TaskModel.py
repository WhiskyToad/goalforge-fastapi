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
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="tasks")
    completed_instances = relationship("CompletedTask", back_populates="task")
    failed_instances = relationship("FailedTask", back_populates="task")


class TaskInstance(EntityMeta):
    __tablename__ = "task_instances"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True, default=None)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    due_date = Column(DateTime)
    status = Column(String, default="pending")


class CompletedTask(EntityMeta):
    __tablename__ = "completed_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed_at = Column(DateTime, default=datetime.utcnow)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="completed_instances")


class FailedTask(EntityMeta):
    __tablename__ = "failed_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    failed_at = Column(DateTime, default=datetime.utcnow)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="failed_instances")
