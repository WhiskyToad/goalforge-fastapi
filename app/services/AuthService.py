from fastapi import Depends
from app.repositories.UserRepository import UserRepository
from app.models.UsersModel import UserModel
from typing import Type
from app.utils.security import verify_password
from app.services.JwtService import jwt_service


class AuthService:
    user_repository: Type[UserRepository]

    def __init__(
        self, user_repository: Type[UserRepository] = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str):
        # Call repository to get user
        user = self.user_repository.get_user(username)

        # Validate credentials
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Incorrect username or password")

        return user

    def create_access_token(self, data: dict):
        # Call external service to create an access token
        return jwt_service.create_access_token(data)
