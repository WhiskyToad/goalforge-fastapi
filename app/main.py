from fastapi import FastAPI
from app.routers.UserRoutes import UserRouter

app = FastAPI()

app.include_router(UserRouter)
