from sqlalchemy.orm import Session

from src.repository.base_repository import BaseRepository
from src.models.party import Party


class PartyRepository(BaseRepository[Party]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Party)
