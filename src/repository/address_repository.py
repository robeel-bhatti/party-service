from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.models.address import Address


class AddressRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Address:
        return self.session.get_one(entity=Address, ident=id)

    def add(self, entity: Address) -> None:
        self.session.add(entity)

    def delete(self, id: int) -> None:
        self.session.delete(instance=Address)

    def get_by_hash(self, hash: str) -> Address | None:
        return self.session.execute(
            select(Address).where(Address.hash == hash)
        ).scalar()
