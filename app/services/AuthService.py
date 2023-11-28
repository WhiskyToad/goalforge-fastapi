from fastapi import Depends, HTTPException, status
from app.repositories.UserRepository import UserRepository
from typing import Type
from app.utils.security import SecurityUtils
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.services.JwtService import JwtService

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    user_repository: Type[UserRepository]

    def __init__(
        self, user_repository: Type[UserRepository] = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
        jwt_service: JwtService = Depends(JwtService),
    ):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt_service.create_access_token(
            {"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def authenticate_user(
        self,
        username: str,
        password: str,
        security_utils: SecurityUtils = Depends(SecurityUtils),
    ):
        # Call repository to get user
        user = self.user_repository.get_user(username)

        # Validate credentials
        if not user or not security_utils.verify_password(
            password, user.hashed_password
        ):
            return False

        return user

    def create_access_token(
        self,
        data: dict,
        jwt_service: JwtService = Depends(JwtService),
    ):
        # Call external service to create an access token
        return jwt_service.create_access_token(data)
