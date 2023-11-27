from fastapi import Depends, HTTPException, status, APIRouter
from app.services.UserService import UserService
from app.schemas.UserSchema import User, UserSignup
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.UsersModel import UserModel

UserRouter = APIRouter(prefix="/api/user", tags=["user"])


@UserRouter.post("/signup", response_model=User)
def signup(user_details: UserSignup, user_service: UserService = Depends(UserService)):
    user = user_service.signup(user_details).normalize()
    return user
