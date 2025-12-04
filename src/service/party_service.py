from typing import Any

from redis import RedisError

from dto.request_dtos import MetaCreate, MetaUpdate
from src.dto.request_dtos import AddressCreate, AddressUpdate
from src.util.enums import ServiceEntities
from src.repository.cache_repository import CacheRepository
from src.dto.request_dtos import PartyCreate, PartyUpdate
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

    def add_party(self, party_request: PartyCreate) -> dict[str, Any]:
        """Create a new party.

        One key piece of business logic is ensuring addresses stay unique.
        If the address in the request payload already exists in the database,
        assign its FK to the new Party.
        If the address does not exist, create it then assign its FK to the new party.

        Every party creation transaction is atomic.
        """
        with self._uow:
            address = self._get_address_or_create(
                party_request.address, party_request.meta
            )
            party = mappers.to_party(party_request)
            party.address = address
            self._create_party(party)
            self._create_party_history(mappers.to_party_history(party))
            party_response = mappers.to_party_response(party).to_dict()

        self._write_to_cache(party.id, party_response)
        logger.info(f"Party with ID {party.id} successfully created.")
        return party_response

    def update_party(self, party_id: int, party_request: PartyUpdate) -> dict[str, Any]:
        was_updated = False

        with self._uow:
            party = self._get_party_by_id(party_id)

            if address_request := party_request.address:
                updated_address_fields = address_request.model_dump(exclude_unset=True)
                all_fields = {field for field in address_request.model_fields.keys()}
                unset_fields = all_fields.difference(set(updated_address_fields.keys()))

                for f in unset_fields:
                    setattr(address_request, f, getattr(party.address, f))

                address = self._get_address_or_create(
                    address_request, party_request.meta
                )
                if address.id != party.address.id:
                    party.address = address
                    was_updated = True

            updated_party_fields = party_request.model_dump(
                exclude_unset=True, exclude={"address", "meta"}
            )

            if updated_party_fields:
                for f in updated_party_fields:
                    if getattr(party, f) != updated_party_fields[f]:
                        was_updated = True
                        setattr(party, f, updated_party_fields[f])

            if was_updated:
                party.updated_by = party_request.meta.updated_by
                self._uow.flush()
                self._create_party_history(mappers.to_party_history(party))
                party_response = mappers.to_party_response(party).to_dict()
                self._write_to_cache(party.id, party_response)
                logger.info(f"Party with ID {party.id} successfully updated.")
                return party_response
            else:
                logger.debug(
                    f"There was nothing to update, so returning back Party with ID {party.id}"
                )
                party_response = mappers.to_party_response(party).to_dict()
                return party_response

    def _get_address_or_create(
        self,
        address_request: AddressCreate | AddressUpdate,
        meta: MetaCreate | MetaUpdate,
    ) -> Address:
        address = self._get_address_by_hash(address_request.get_hash())

        if address is None:
            address = mappers.to_address(address_request)
            if isinstance(address_request, AddressCreate):
                address.created_by = meta.created_by
                address.updated_by = meta.created_by
            elif isinstance(address_request, PartyUpdate):
                address.created_by = meta.updated_by
                address.updated_by = meta.updated_by
            self._create_address(address)

        return address

    def _create_party(self, party: Party) -> None:
        logger.debug("Inserting new Party into database.")
        self._uow.party_repository.add(party)
        self._uow.flush()

    def _create_address(self, address: Address) -> None:
        logger.debug("Inserting new Address into database.")
        self._uow.address_repository.add(address)
        self._uow.flush()

    def _create_party_history(self, party_history: PartyHistory) -> None:
        logger.debug(
            f"Inserting new Party History for Party {party_history.party_id} into database."
        )
        self._uow.party_history_repository.add(party_history)
        self._uow.flush()

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
