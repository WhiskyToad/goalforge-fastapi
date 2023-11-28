from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.errors.NotAuthorizedError import NotAuthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise NotAuthorizedError()
    except JWTError:
        raise NotAuthorizedError()
    return int(user_id)
