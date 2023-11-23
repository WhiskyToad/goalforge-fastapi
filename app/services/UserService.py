from fastapi import Depends
from app.repositories.UserRepository import UserRepository
from app.models.UsersModel import UserModel
from app.schemas.UserSchema import UserSignup
from typing import Type


class UserService:
    user_repository: Type[UserRepository]

    def __init__(
        self, user_repository: Type[UserRepository] = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def signup(self, user_details: UserSignup) -> UserModel:
        user = UserModel(email=user_details.email, password=user_details.password)
        return self.user_repository.create(user)
