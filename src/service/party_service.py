from typing import Any

from redis import RedisError

from src.util.enums import ServiceEntities
from src.repository.cache_repository import CacheRepository
from src.dto.request_dtos import PartyRequest
from src.util import mappers
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory
from src.repository.unit_of_work import UnitOfWork
import logging

logger = logging.getLogger(__name__)


class PartyService:
    """Orchestrate all business logic for the Party entity."""

    def __init__(self, unit_of_work: UnitOfWork, cache_repository: CacheRepository):
        self._uow = unit_of_work
        self._cache_repository = cache_repository

    def get_party(self, party_id: int) -> dict[str, Any]:
        """Get a party entity by ID and write the entity to the cache."""
        party = self._get_party_by_id(party_id)
        party_response = mappers.to_party_response(party).to_dict()
        self._write_to_cache(party.id, party_response)
        return party_response

    def add_party(self, party_request: PartyRequest) -> dict[str, Any]:
        """Create a new party.

        One key piece of business logic is ensuring addresses stay unique.
        If the address in the request payload already exists in the database,
        assign its FK to the new Party.
        If the address does not exist, create it then assign its FK to the new party.

        Every party creation transaction is atomic.
        """
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
            party_response = mappers.to_party_response(party).to_dict()

        self._write_to_cache(party.id, party_response)
        logger.info(f"Party with ID {party.id} successfully created.")
        return party_response

    def _create_party(self, party: Party) -> Party:
        logger.debug("Inserting new Party into database.")
        self._uow.party_repository.add(party)
        self._uow.flush()
        return party

    def _create_address(self, address: Address) -> Address:
        logger.debug("Inserting new Address into database.")
        self._uow.address_repository.add(address)
        self._uow.flush()
        return address

    def _create_party_history(self, party_history: PartyHistory) -> PartyHistory:
        logger.debug(
            f"Inserting new Party History for Party {party_history.party_id} into database."
        )
        self._uow.party_history_repository.add(party_history)
        self._uow.flush()
        return party_history

    def _get_address_by_hash(self, address_hash: str) -> Address | None:
        logger.debug(f"Getting Address with hash: {address_hash} from database.")
        return self._uow.address_repository.get_by_hash(address_hash)

    def _get_party_by_id(self, party_id: int) -> Party:
        logger.debug(f"Getting Party with ID: {party_id} from database.")
        return self._uow.party_repository.get_by_id(party_id)

    def _write_to_cache(self, party_id: int, res: dict[str, Any]) -> None:
        logger.debug(f"Writing Party with ID: {party_id} into cache.")
        try:
            self._cache_repository.add(party_id, ServiceEntities.PARTY, res)
        except RedisError as e:
            logger.warning(
                f"Could not write Party with ID {party_id} to cache due to Redis Error: {e}."
            )
