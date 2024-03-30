from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.config.Database import get_db_connection


class GoalsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db
