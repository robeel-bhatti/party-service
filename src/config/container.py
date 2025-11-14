from typing import Optional

from sqlalchemy.orm import Session

from src.repository.address_repository import AddressRepository
from src.repository.party_history_repository import PartyHistoryRepository
from src.repository.party_repository import PartyRepository
from src.repository.unit_of_work import UnitOfWork
from src.service.party_service import PartyService


class Container:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self._party_repository: Optional[PartyRepository] = None
        self._address_repository: Optional[AddressRepository] = None
        self._party_history_repository: Optional[PartyHistoryRepository] = None
        self._party_service: Optional[PartyService] = None
        self._unit_of_work: Optional[UnitOfWork] = None

    @property
    def party_history_repository(self) -> PartyHistoryRepository:
        if not self._party_history_repository:
            self._party_history_repository = PartyHistoryRepository(self.db_session)
        return self._party_history_repository

    @property
    def party_repository(self) -> PartyRepository:
        if not self._party_repository:
            self._party_repository = PartyRepository(self.db_session)
        return self._party_repository

    @property
    def address_repository(self) -> AddressRepository:
        if not self._address_repository:
            self._address_repository = AddressRepository(self.db_session)
        return self._address_repository

    @property
    def unit_of_work(self) -> UnitOfWork:
        if not self._unit_of_work:
            self._unit_of_work = UnitOfWork(
                self.db_session,
                self.party_repository,
                self.address_repository,
                self.party_history_repository,
            )
        return self._unit_of_work

    @property
    def party_service(self) -> PartyService:
        if not self._party_service:
            self._party_service = PartyService(self.unit_of_work)
        return self._party_service
