from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
