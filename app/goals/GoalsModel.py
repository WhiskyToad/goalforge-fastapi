from datetime import datetime, timezone
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column

from app.shared.models.BaseModel import EntityMeta


class GoalModel(EntityMeta):
    __tablename__ = "goals"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    description = mapped_column(String)
    is_completed = mapped_column(Boolean, default=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    target_date = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    user_id = mapped_column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="goals")
    tasks = relationship("Task", secondary="goal_tasks", back_populates="goals")


class GoalTask(EntityMeta):
    __tablename__ = "goal_tasks"

    goal_id = mapped_column(Integer, ForeignKey("goals.id"), primary_key=True)
    task_id = mapped_column(Integer, ForeignKey("tasks.id"), primary_key=True)

    goal = relationship("GoalModel", back_populates="tasks")
    task = relationship("Task", back_populates="goals")
