from fastapi import Depends, APIRouter
from app.services.UserService import UserService
from app.schemas.UserSchema import User, UserSignup
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.JwtSchema import Token
from app.services.AuthService import AuthService
from app.utils.auth import get_user_id_from_token


UserRouter = APIRouter(prefix="/api/user", tags=["user"])


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@UserRouter.post("/signup", response_model=Token)
async def signup(
    user_details: UserSignup, user_service: UserService = Depends(UserService)
):
    token = await user_service.signup(user_details)
    return token


@UserRouter.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.login(form_data)


@UserRouter.get("/me")
async def read_users_me(
    user_id: str = Depends(get_user_id_from_token),
    user_service: UserService = Depends(UserService),
):
    return user_service.get_current_user(user_id)
