from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.BaseModel import EntityMeta


class UserModel(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
