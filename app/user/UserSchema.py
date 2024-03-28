from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: str
    id: int
    username: str


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserEditProfile(BaseModel):
    email: EmailStr
    username: str
