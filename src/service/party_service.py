from typing import Any

from src.dto.address_dto import AddressDTO
from src.dto.party_dto import PartyDTO
from src.mapper.mappers import to_address_model, to_party_history_model, to_party_model
from src.models.address import Address
from src.models.party import Party
from src.repository.abstract_repository import AbstractRepository
from src.repository.party_history_repository import PartyHistoryRepository
from src.repository.unit_of_work import UnitOfWork


class PartyService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        party_repository: AbstractRepository[Party],
        address_repository: AbstractRepository[Address],
        party_history_repository: PartyHistoryRepository,
    ):
        self.unit_of_work = unit_of_work
        self.party_repository = party_repository
        self.address_repository = address_repository
        self.party_history_repository = party_history_repository

    def add_party(self, req: dict[str, Any]) -> dict[str, Any]:
        party_dto = PartyDTO(**req)
        address_dto = party_dto.address
        created_by = party_dto.meta.created_by

        with self.unit_of_work:
            address = self._get_or_create_address(address_dto, created_by)
            party = self._create_party(party_dto, address.id, created_by)
            self._create_party_history(party, address, created_by)
            party_dto.id = party.id
            address_dto.id = address.id
            return party_dto.model_dump()

    def _create_party(
        self, party_dto: PartyDTO, address_id: int, created_by: str
    ) -> Party:
        party_hash = party_dto.get_hash()
        party = to_party_model(party_dto)
        party.hash = party_hash
        party.address_id = address_id
        party.created_by = created_by
        party.updated_by = created_by
        self.party_repository.add(party)
        self.unit_of_work.flush()
        return party

    def _get_or_create_address(
        self, address_dto: AddressDTO, created_by: str
    ) -> Address:
        addr_hash = address_dto.get_hash()
        address = self.address_repository.get_by_hash(addr_hash)

        if address is None:
            address = to_address_model(address_dto)
            address.hash = addr_hash
            address.created_by = created_by
            address.updated_by = created_by
            self.address_repository.add(address)
            self.unit_of_work.flush()

        return address

    def _create_party_history(
        self, party: Party, address: Address, created_by: str
    ) -> None:
        party_history = to_party_history_model(party, address)
        party_history.created_by = created_by
        party_history.updated_by = created_by
        self.party_history_repository.add(party_history)
