from .CustomError import CustomError


class NotAuthorizedError(CustomError):
    def __init__(self):
        super().__init__("You are not authorized", status_code=401)
