from typing import Any
from src.config.enums import ServiceEntities
from src.repository.cache_repository import CacheRepository
from src.dto.request_dtos import PartyRequest
from src.mapper import mappers
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory
from src.repository.unit_of_work import UnitOfWork
import logging
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class PartyService:
    """Orchestrate all business logic for the Party entity."""

    def __init__(self, unit_of_work: UnitOfWork, cache_repository: CacheRepository):
        self._uow = unit_of_work
        self._cache_repository = cache_repository

    def add_party(self, req: dict[str, Any]) -> dict[str, Any]:
        """Create a new party.

        One key piece of business logic is ensuring addresses stay unique.
        If the address in the request payload already exists in the database,
        assign its FK to the new Party.
        If the address does not exist, create it then assign its FK to the new party.

        Every party creation transaction is atomic.
        """
        party_request = PartyRequest(**req)
        with self._uow:
            address = self._get_address_by_hash(party_request.address.get_hash())
            if address is None:
                address = self._create_address(
                    mappers.to_address(party_request.address)
                )

            party = mappers.to_party(party_request)
            party.address_id = address.id
            party = self._create_party(party)

            party_history = mappers.to_party_history(party, address)
            self._create_party_history(party_history)
            party_response = mappers.to_party_response(party, address).to_dict()

        try:
            self._cache_repository.add(party.id, ServiceEntities.PARTY, party_response)
            logger.debug(f"Party with ID {id} saved in cache.")
        except RedisError as e:
            logger.warning(f"Error caching Party with ID {party.id}: {e}")

        logger.info(f"Party with ID {party.id} successfully created.")
        return party_response

    def _create_party(self, party: Party) -> Party:
        logger.debug("Inserting new party into database.")
        self._uow.party_repository.add(party)
        self._uow.flush()
        return party

    def _create_address(self, address: Address) -> Address:
        logger.debug("Inserting new address into database.")
        self._uow.address_repository.add(address)
        self._uow.flush()
        return address

    def _create_party_history(self, party_history: PartyHistory) -> PartyHistory:
        logger.debug(
            f"Inserting new party history for Party {party_history.party_id} into database."
        )
        self._uow.party_history_repository.add(party_history)
        self._uow.flush()
        return party_history

    def _get_address_by_hash(self, address_hash: str) -> Address | None:
        logger.debug(f"Getting address from hash: {address_hash}")
        return self._uow.address_repository.get_by_hash(address_hash)
