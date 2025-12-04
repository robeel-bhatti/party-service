import logging
from typing import Any
from redis import RedisError
from src.dto.request_dtos import MetaCreate, MetaUpdate
from src.dto.request_dtos import AddressCreate, AddressUpdate
from src.util.enums import ServiceEntities
from src.repository.cache_repository import CacheRepository
from src.dto.request_dtos import PartyCreate, PartyUpdate
from src.util import mappers
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory
from src.repository.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class PartyService:
    """Orchestrate all business logic for the Party entity.

    This business logic currently entails getting a Party by ID, updating a Party (PATCH),
    and creating a new Party (POST).
    """

    def __init__(self, unit_of_work: UnitOfWork, cache_repository: CacheRepository):
        self._uow = unit_of_work
        self._cache_repository = cache_repository

    def get_party(self, party_id: int) -> dict[str, Any]:
        """
        Get a Party by ID from the database, and then write the Party to the cache afterward.
        The reason the cache write occurs is that if the code gets to this point, then
        the cache_read decorator resulted in a cache miss.
        """
        party = self._get_party_by_id(party_id)
        party_response = mappers.to_party_response(party).to_dict()
        self._write_to_cache(party.id, party_response)
        return party_response

    def add_party(self, party_request: PartyCreate) -> dict[str, Any]:
        """Create a new Party.

        Create a new Party History at the end, and then write the Party to the cache.
        Then return the newly created Party alongside its Address information.

        The cache write occurs outside the transaction, as we don't want the transaction to rollback
        if the cache write fails. At least retain the newly created Party in the database at that point.
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
        """
        Update an existing Party.

        First determine are there are any address fields to update in the request.
        If so, grab the address fields which were NOT SET in the request from the entity,
        and set those values onto the request pydantic model. This is so we now have the
        updated address and all of its components on our pydantic model, and now we can calculate its hash
        and start our usual address validation flow.

        Then determine are there any party attributes that are in the request payload.
        If they are, set them on the Party entity. But only set them if their value is not equal to the
        existing value for the same field.

        This update is atomic, and so all database changes must be committed together.

        To maintain idempotency, if nothing was updated, the party entity will not be updated,
        and it will be returned as is.
        """
        # use this flag to ensure we actually updated the entity
        # we will need this at the end.
        was_updated = False

        with self._uow:
            party = self._get_party_by_id(party_id)

            if address_request := party_request.address:
                #### Address Update Flow #####
                updated_address_fields = address_request.model_dump(exclude_unset=True)
                all_fields = {field for field in address_request.model_fields.keys()}
                unset_fields = all_fields.difference(set(updated_address_fields.keys()))

                for f in unset_fields:
                    setattr(address_request, f, getattr(party.address, f))

                address = self._get_address_or_create(
                    address_request, party_request.meta
                )
                # doublecheck the IDs are actually different
                if address.id != party.address.id:
                    party.address = address
                    was_updated = True

            #### Party Update Flow #####
            updated_party_fields = party_request.model_dump(
                exclude_unset=True, exclude={"address", "meta"}
            )

            if updated_party_fields:
                for f in updated_party_fields:
                    if getattr(party, f) != updated_party_fields[f]:
                        was_updated = True
                        setattr(party, f, updated_party_fields[f])

            #### Final Update Logic #####
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
        """
        Given the address portion of the request payload during a PATCH or POST,
        determine if the address already exists in the database via the calculated hash.

        If the address exists, then return it.
        If the address does not exist, create it and then return it.
        """
        addr_hash = address_request.get_hash()
        address = self._get_address_by_hash(addr_hash)

        if address is None:
            logger.debug(
                f"Address with hash: {addr_hash} does not exist so creating new Address."
            )
            address = mappers.to_address(address_request)
            if isinstance(meta, MetaCreate):
                address.created_by = meta.created_by
                address.updated_by = meta.created_by
            elif isinstance(meta, MetaUpdate):
                address.created_by = meta.updated_by
                address.updated_by = meta.updated_by
            self._create_address(address)

        return address

    def _create_party(self, party: Party) -> None:
        """
        Create a Party record, and flush afterward to have pending database changes
        in the Party entity.
        """
        logger.debug("Inserting new Party into database.")
        self._uow.party_repository.add(party)
        self._uow.flush()

    def _create_address(self, address: Address) -> None:
        """
        Create an Address record, and flush afterward to have pending database changes
        to the Address entity.
        """
        logger.debug("Inserting new Address into database.")
        self._uow.address_repository.add(address)
        self._uow.flush()

    def _create_party_history(self, party_history: PartyHistory) -> None:
        """
        Create a Party History record, and flush afterward to have pending database changes
        in the Party History entity.
        """
        logger.debug(
            f"Inserting new Party History for Party {party_history.party_id} into database."
        )
        self._uow.party_history_repository.add(party_history)
        self._uow.flush()

    def _get_address_by_hash(self, address_hash: str) -> Address | None:
        """
        Get an address by the provided SHA-256 hex-encoded hash string.
        """
        logger.debug(f"Getting Address with hash: {address_hash} from database.")
        return self._uow.address_repository.get_by_hash(address_hash)

    def _get_party_by_id(self, party_id: int) -> Party:
        """
        Get a Party from the database via the provided ID.
        """
        logger.debug(f"Getting Party with ID: {party_id} from database.")
        return self._uow.party_repository.get_by_id(party_id)

    def _write_to_cache(self, party_id: int, res: dict[str, Any]) -> None:
        """
        Write the party to the cache.
        The party is written to the cache when the party is updated, newly created, or when the party
        was retrieved from the database after a cache miss.
        """
        logger.debug(f"Writing Party with ID: {party_id} into cache.")
        try:
            self._cache_repository.add(party_id, ServiceEntities.PARTY, res)
        except RedisError as e:
            logger.warning(
                f"Could not write Party with ID {party_id} to cache due to Redis Error: {e}."
            )
