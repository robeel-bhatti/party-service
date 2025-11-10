from sqlalchemy.orm import Session

from src.models.party import Party
from src.repository.abstract_repository import AbstractRepository


class PartyRepository(AbstractRepository[Party]):
    def __init__(self, session: Session):
        self.session = session

    # def get_all(self, query: str) -> list[Party]:
    #     pass

    def get_by_id(self, id: int) -> Party:
        return self.session.get_one(entity=Party, ident=id)

    def add(self, entity: Party) -> None:
        self.session.add(entity)

    def delete(self, id: int) -> None:
        self.session.delete(instance=Party)

    def get_by_hash(self, name: str) -> Party:
        raise NotImplementedError
