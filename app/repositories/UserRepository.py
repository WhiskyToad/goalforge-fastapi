from fastapi import Depends
from app.models.UsersModel import UserModel
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection
from app.schemas.UserSchema import User


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return User(id=user.id, email=user.email)

    # def get_by_email(self, email: str):
    #     # Your repository retrieval logic here
    #     pass
