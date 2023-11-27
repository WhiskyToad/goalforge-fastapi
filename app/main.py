from app.routers.UserRoutes import UserRouter
from fastapi import FastAPI


app = FastAPI()


app.include_router(UserRouter)
