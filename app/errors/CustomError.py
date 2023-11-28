from typing import List


class CustomError(Exception):
    def __init__(self, message: str, status_code: int = 400, errors: List[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors or [{"message": message}]

    def serialize_errors(self):
        return self.errors
