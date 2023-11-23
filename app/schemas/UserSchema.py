from pydantic import BaseModel


class User(BaseModel):
    email: str
    id: int


class UserSignup(BaseModel):
    email: str
    password: str
