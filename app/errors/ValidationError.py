from app.main import app
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


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
