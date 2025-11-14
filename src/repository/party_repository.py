from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.models.party import Party


class PartyRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Party:
        return self.session.get_one(entity=Party, ident=id)

    def add(self, entity: Party) -> None:
        self.session.add(entity)

    def delete(self, id: int) -> None:
        self.session.delete(instance=Party)

    def get_by_hash(self, hash: str) -> Party | None:
        return self.session.execute(select(Party).where(Party.hash == hash)).scalar()
