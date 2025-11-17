from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.repository.base_repository import BaseRepository
from src.models.address import Address


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Address)

    def get_by_hash(self, hash: str) -> Address | None:
        return self.session.execute(
            select(Address).where(Address.hash == hash)
        ).scalar()
