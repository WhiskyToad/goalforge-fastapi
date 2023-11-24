from sqlalchemy import Column, Integer, String
from app.models.BaseModel import EntityMeta
from app.schemas.UserSchema import User


class UserModel(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)

    def normalize(self) -> User:
        return {
            "id": self.id.__str__(),
            "email": self.email.__str__(),
        }
