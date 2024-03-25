from app.user.UserRoutes import UserRouter
from app.task.TaskRoutes import TaskRouter
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

load_dotenv()

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: RequestValidationError):
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
app.include_router(TaskRouter)
