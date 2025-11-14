from typing import Any

from src.dto.address_dto import AddressDTO
from src.dto.party_dto import PartyDTO
from src.mapper.mappers import to_address_model, to_party_history_model, to_party_model
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory
from src.repository.unit_of_work import UnitOfWork
from src.exception.custom_exceptions import EntityAlreadyExistsError
import logging

logger = logging.getLogger(__name__)


class PartyService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work

    def add_party(self, req: dict[str, Any]) -> dict[str, Any]:
        party_dto = PartyDTO(**req)
        party_hash = party_dto.get_hash()
        existing_party = self.uow.party_repository.get_by_hash(party_hash)
        if existing_party:
            msg = f"Failed to create Party because Party already exists with ID: {existing_party.id}"
            logger.error(f"{msg} and hash: {party_hash}")
            raise EntityAlreadyExistsError(msg)

        address_dto = party_dto.address
        created_by = party_dto.meta.created_by

        with self.uow:
            address = self._get_or_create_address(address_dto, created_by)
            party = self._create_party(party_dto, address.id, created_by, party_hash)
            self._create_party_history(party, address, created_by)
            party_dto.id = party.id
            address_dto.id = address.id
            return party_dto.model_dump()

    def _create_party(
        self, party_dto: PartyDTO, address_id: int, created_by: str, party_hash: str
    ) -> Party:
        party = to_party_model(party_dto)
        party.hash = party_hash
        party.address_id = address_id
        party.created_by = created_by
        party.updated_by = created_by
        self.uow.party_repository.add(party)
        self.uow.flush()
        return party

    def _get_or_create_address(
        self, address_dto: AddressDTO, created_by: str
    ) -> Address:
        addr_hash = address_dto.get_hash()
        address = self.uow.address_repository.get_by_hash(addr_hash)

        if address is None:
            address = to_address_model(address_dto)
            address.hash = addr_hash
            address.created_by = created_by
            address.updated_by = created_by
            self.uow.address_repository.add(address)
            self.uow.flush()

        return address

    def _create_party_history(
        self, party: Party, address: Address, created_by: str
    ) -> PartyHistory:
        party_history = to_party_history_model(party, address)
        party_history.created_by = created_by
        party_history.updated_by = created_by
        self.uow.party_history_repository.add(party_history)
        return party_history
