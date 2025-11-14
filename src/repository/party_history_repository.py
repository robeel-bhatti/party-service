from sqlalchemy.orm import Session

from src.models.party_history import PartyHistory


class PartyHistoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, party_history: PartyHistory) -> None:
        self.session.add(party_history)
