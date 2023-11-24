from fastapi import FastAPI
from app.routers.UserRoutes import UserRouter
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(UserRouter)
