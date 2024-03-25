from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.BaseModel import EntityMeta


class TaskCategory(EntityMeta):
    __tablename__ = "task_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Ensure name is unique per owner
    __table_args__ = (UniqueConstraint("name", "owner_id"),)

    tasks = relationship("Task", back_populates="category")
