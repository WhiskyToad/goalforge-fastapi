from fastapi import Depends
from app.repositories.UserRepository import UserRepository
from app.models.UsersModel import UserModel
from app.schemas.UserSchema import UserSignup
from typing import Type
from datetime import datetime, timedelta
from jose import JWTError, jwt


class UserService:
    user_repository: Type[UserRepository]

    def __init__(
        self, user_repository: Type[UserRepository] = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def signup(self, user_details: UserSignup) -> UserModel:
        user = UserModel(email=user_details.email, password=user_details.password)
        return self.user_repository.create(user)

    def authenticate_user(fake_db, username: str, password: str):
        user = get_user(fake_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
