from fastapi import Depends, HTTPException, status
from app.repositories.UserRepository import UserRepository
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserSignup
from typing import Type
from jose import JWTError, jwt
from typing import Annotated
from app.schemas.JwtSchema import TokenData
from datetime import timedelta
from app.services.JwtService import JwtService
from app.utils.security import SecurityUtils


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class UserService:
    user_repository: Type[UserRepository]
    security_utils: Type[SecurityUtils]

    def __init__(
        self,
        user_repository: Type[UserRepository] = Depends(UserRepository),
        security_utils: SecurityUtils = Depends(SecurityUtils),
    ) -> None:
        self.user_repository = user_repository
        self.security_utils = security_utils

    async def signup(
        self,
        user_details: UserSignup,
        jwt_service: JwtService = Depends(JwtService),
    ):
        hashed_password = self.security_utils.get_password_hash(user_details.password)
        user = await self.user_repository.create(
            UserModel(
                email=user_details.email,
                hashed_password=hashed_password,
                username=user_details.username,
            )
        )
        access_token_expires = timedelta(minutes=30)
        access_token = jwt_service.create_access_token(
            {"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: Annotated[str, Depends()]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.user_repository.get_user_by_id(username=token_data.id)
        if user is None:
            raise credentials_exception
        return user
