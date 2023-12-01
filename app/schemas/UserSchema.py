from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: str
    id: int


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    username: str
