from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.errors.CustomError import CustomError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("JWT_ALGORITHM")


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise CustomError(
                status_code=400, message="Invalid input", code="INVALID_INPUT"
            )
    except JWTError:
        raise CustomError(
            status_code=400, message="Invalid input", code="INVALID_INPUT"
        )
    return int(user_id)
