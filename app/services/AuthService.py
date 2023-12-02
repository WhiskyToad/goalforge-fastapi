from fastapi import Depends, status
from app.repositories.UserRepository import UserRepository
from typing import Type
from app.utils.security import SecurityUtils
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.services.JwtService import JwtService
from app.errors.CustomError import CustomError


class AuthService:
    user_repository: Type[UserRepository]
    security_utils: Type[SecurityUtils]
    jwt_service: Type[JwtService]

    def __init__(
        self,
        user_repository: Type[UserRepository] = Depends(UserRepository),
        security_utils: SecurityUtils = Depends(SecurityUtils),
        jwt_service: JwtService = Depends(JwtService),
    ) -> None:
        self.user_repository = user_repository
        self.security_utils = security_utils
        self.jwt_service = jwt_service

    async def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise CustomError(
                status_code=400, message="Invalid input", code="INVALID_INPUT"
            )
        access_token_expires = timedelta(minutes=30)
        access_token = self.jwt_service.create_access_token(
            {"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def authenticate_user(
        self,
        email: str,
        password: str,
    ):
        # Call repository to get user
        user = self.user_repository.get_user_by_email(email)

        # Validate credentials
        if not user or not self.security_utils.verify_password(
            password, user.hashed_password
        ):
            return False

        return user
