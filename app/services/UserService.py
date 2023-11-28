from fastapi import Depends, HTTPException, status
from app.repositories.UserRepository import UserRepository
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserSignup
from typing import Type
from jose import JWTError, jwt
from app.schemas.JwtSchema import TokenData
from datetime import timedelta
from app.services.JwtService import JwtService
from app.utils.security import SecurityUtils


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class UserService:
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

    async def signup(
        self,
        user_details: UserSignup,
    ):
        hashed_password = self.security_utils.get_password_hash(user_details.password)
        user = self.user_repository.create(
            UserModel(
                email=user_details.email,
                hashed_password=hashed_password,
                username=user_details.username,
            )
        )
        access_token_expires = timedelta(minutes=30)
        access_token = self.jwt_service.create_access_token(
            {"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def get_current_user(self, user_id: int):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user
