from fastapi import Depends
from app.models.UserModel import UserModel
from sqlalchemy.orm import Session
from app.config.Database import get_db_connection


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.email == email).first()
