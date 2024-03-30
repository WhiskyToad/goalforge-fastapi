from sqlalchemy import Integer, String
from app.shared.models.BaseModel import EntityMeta
from sqlalchemy.orm import relationship, mapped_column
from app.goals.GoalsModel import *


class UserModel(EntityMeta):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, index=True)
    username = mapped_column(String, index=True)
    hashed_password = mapped_column(String)

    tasks = relationship("Task", back_populates="owner")
    goals = relationship("GoalModel", back_populates="owner")
