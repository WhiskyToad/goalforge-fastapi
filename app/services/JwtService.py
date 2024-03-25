from datetime import timedelta, datetime, timezone
from typing import Any, Dict, Optional
from jose import jwt
import os

SECRET_KEY = os.environ.get("JWT_SECRET", "")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "")


class JwtService:
    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
