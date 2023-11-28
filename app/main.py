from app.routers.UserRoutes import UserRouter
from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


app.include_router(UserRouter)
