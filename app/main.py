from app.routers.UserRoutes import UserRouter
from fastapi import FastAPI
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

load_dotenv()

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request, exc):
    errors = exc.errors()
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {"message": error["msg"], "code": error["type"]} for error in errors
            ]
        },
    )


app.include_router(UserRouter)
