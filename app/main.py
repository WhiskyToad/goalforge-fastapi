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
        # TODO loop this and return an array, add field in code part
        content={"detail": {"message": errors[0]["msg"]}},
    )


app.include_router(UserRouter)
