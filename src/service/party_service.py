from typing import Any

from src.dto.party_dto import PartyDTO
from src.mapper.mappers import to_address_model
from src.models.address import Address
from src.models.party import Party
from src.repository.abstract_repository import AbstractRepository
from src.repository.unit_of_work import UnitOfWork


class PartyService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        party_repository: AbstractRepository[Party],
        address_repository: AbstractRepository[Address],
    ):
        self.unit_of_work = unit_of_work
        self.party_repository = party_repository
        self.address_repository = address_repository

    def add_party(self, req: dict[str, Any]) -> None:
        party_dto = PartyDTO(**req)
        address_dto = party_dto.address
        meta_dto = party_dto.meta

        addr_hash = address_dto.get_hash()

        with self.unit_of_work:
            address = self.address_repository.get_by_hash(addr_hash)

            if address is None:
                address = to_address_model(address_dto)
                address.hash = addr_hash
                address.created_by = meta_dto.created_by
                address.updated_by = meta_dto.created_by
                self.address_repository.add(address)
                self.unit_of_work.flush()
