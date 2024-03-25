from sqlalchemy import Column, Integer, String
from app.models.BaseModel import EntityMeta
from sqlalchemy.orm import relationship


class UserModel(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner")
