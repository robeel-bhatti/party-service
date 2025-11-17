from sqlalchemy.orm import Session

from src.repository.base_repository import BaseRepository
from src.models.party_history import PartyHistory


class PartyHistoryRepository(BaseRepository[PartyHistory]):
    """Data access layer for party history entities."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, PartyHistory)
