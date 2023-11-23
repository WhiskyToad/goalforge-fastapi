from fastapi import APIRouter, Depends
from app.services.UserService import UserService
from app.schemas.UserSchema import User, UserSignup

UserRouter = APIRouter(prefix="/api/user", tags=["user"])


@UserRouter.post("/signup", response_model=User)
def signup(user_details: UserSignup, user_service: UserService = Depends(UserService)):
    user = user_service.signup(user_details).normalize()
    return user
