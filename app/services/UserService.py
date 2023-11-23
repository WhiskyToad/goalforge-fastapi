from fastapi import Depends
from typing import Type
from app.repositories.UserRepository import UserRepository
from app.models.UsersModel import UserModel


class UserService:
    user_repository: Type[UserRepository]

    def __init__(self, user_repository: Type[UserRepository] = Depends()) -> None:
        self.user_repository = user_repository

    def signup(self, email: str, password: str) -> UserModel:
        user = self.user_repository.create(UserModel(email, password))
        return user

    # def login(self, email: str, password: str) -> UserModel:
    #     user = self.user_repository.email(email)
    #     if user and user.check_password(password):
    #         return user
    #     return None
