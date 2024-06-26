from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, timezone
from app.shared.models.BaseModel import EntityMeta
from app.task.TaskSchema import TaskInstanceStatus


class Task(EntityMeta):
    __tablename__ = "tasks"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    icon = mapped_column(String, index=True, default="")
    description = mapped_column(String)
    recurring = mapped_column(Boolean, default=False)
    recurring_interval = mapped_column(String, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    is_habit = mapped_column(Boolean, default=False)

    owner_id = mapped_column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="tasks")

    task_instances = relationship("TaskInstance", back_populates="task")
    goals = relationship("GoalModel", back_populates="tasks", secondary="goal_tasks")


class TaskInstance(EntityMeta):
    __tablename__ = "task_instances"

    id = mapped_column(Integer, primary_key=True, index=True)
    completed = mapped_column(Boolean, default=False)
    completed_at = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    task_id = mapped_column(Integer, ForeignKey("tasks.id"))
    due_date = mapped_column(DateTime(timezone=True))
    status = mapped_column(
        SQLAlchemyEnum(TaskInstanceStatus), default=TaskInstanceStatus.PENDING
    )

    task = relationship("Task", back_populates="task_instances")
