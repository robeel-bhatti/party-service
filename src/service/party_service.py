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

    def get_party(self, party_id: int) -> dict[str, Any]:
        party_response = self._get_party_from_cache(party_id)
        if party_response:
            return party_response

        party = self._get_party_by_id(party_id)
        party_response = mappers.to_party_response(party).to_dict()
        self._write_to_cache(party_id, party_response)
        return party_response

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
            party_response = mappers.to_party_response(party).to_dict()

        self._write_to_cache(party.id, party_response)
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
        logger.debug(f"Getting address with hash: {address_hash} from database.")
        return self._uow.address_repository.get_by_hash(address_hash)

    def _get_party_by_id(self, party_id: int) -> Party:
        logger.debug(f"Getting party with ID: {party_id} from database.")
        return self._uow.party_repository.get_by_id(party_id)

    def _get_party_from_cache(self, party_id: int) -> dict[str, Any] | None:
        logger.debug(f"Getting party with ID: {party_id} from cache.")
        try:
            cached = self._cache_repository.get(party_id, ServiceEntities.PARTY)
            if cached:
                logger.debug(f"Cache hit for Party with ID {party_id}.")
                return cached

            logger.debug(f"Cache miss for Party with ID {party_id}.")
            return None

        except RedisError as e:
            logger.warning(
                f"Could not get Party with ID {party_id} due to Redis Error: {e}"
            )
            return None

    def _write_to_cache(self, party_id: int, res: dict[str, Any]) -> None:
        logger.debug(f"Writing party with ID: {party_id} into cache.")
        try:
            self._cache_repository.add(party_id, ServiceEntities.PARTY, res)
        except RedisError as e:
            logger.warning(
                f"Could not write Party with ID {party_id} to cache due to Redis Error: {e}."
            )
