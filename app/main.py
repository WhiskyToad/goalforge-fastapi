from fastapi import FastAPI
from app.routers.UserRoutes import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/user", tags=["auth"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
