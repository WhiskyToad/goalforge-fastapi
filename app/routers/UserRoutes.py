from fastapi import APIRouter, Depends
from app.services.UserService import UserService
from app.schemas.UserSchema import User

router = APIRouter()


@router.post("/signup", response_model=User)
def signup(email: str, password: str, user_service: UserService = Depends()):
    user = UserService.signup(email, password).normalize()
    return user


# @router.post("/login")
# def login():
#     return {"message": "Login"}
