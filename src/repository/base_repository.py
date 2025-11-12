from sqlalchemy.orm import Session

from src.models.base import Base


class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, entity: Base) -> None:
        self.session.add(entity)
