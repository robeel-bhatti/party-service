from typing import Any

from src.dto.party_dto import PartyDTO
from src.models.address import Address
from src.models.party import Party
from src.repository.abstract_repository import AbstractRepository


class PartyService:
    def __init__(
        self,
        party_repository: AbstractRepository[Party],
        address_repository: AbstractRepository[Address],
    ):
        self.party_repository = party_repository
        self.address_repository = address_repository

    def add_party(self, req: dict[str, Any]) -> None:
        # validate request payload first
        party = PartyDTO(**req)

        # if request is valid, start address validation
        # to do address validation, we need to get the address hash
        party.address.get_hash()

        # then we will query the database for address row with that hash
