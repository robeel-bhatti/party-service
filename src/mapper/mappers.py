from src.dto.request_dtos import PartyRequest, AddressRequest
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory
from src.dto.response_dtos import PartyResponse, AddressResponse, MetaResponse
from src.models.base import Base


def to_party(party_request: PartyRequest) -> Party:
    return Party(
        first_name=party_request.first_name,
        last_name=party_request.last_name,
        middle_name=party_request.middle_name,
        email=str(party_request.email),
        phone_number=str(party_request.phone_number),
        created_by=party_request.meta.created_by,
        updated_by=party_request.meta.created_by,
    )


def to_address(address_request: AddressRequest) -> Address:
    return Address(
        street_one=address_request.street_one,
        street_two=address_request.street_two,
        city=address_request.city,
        state=address_request.state,
        postal_code=address_request.postal_code,
        country=address_request.country,
        hash=address_request.get_hash(),
        created_by=address_request.meta.created_by,
        updated_by=address_request.meta.created_by,
    )


def to_party_history(party: Party, address: Address) -> PartyHistory:
    return PartyHistory(
        party_id=party.id,
        first_name=party.first_name,
        last_name=party.last_name,
        middle_name=party.middle_name,
        email=party.email,
        phone_number=party.phone_number,
        party_created_at=party.created_at,
        party_updated_at=party.updated_at,
        party_created_by=party.created_by,
        party_updated_by=party.updated_by,
        street_one=address.street_one,
        street_two=address.street_two,
        city=address.city,
        state=address.state,
        zip_code=address.postal_code,
        country=address.country,
        created_by=party.created_by,
        updated_by=party.created_by,
    )


def to_meta_response(model: Base) -> MetaResponse:
    """Extract metadata from any model with audit fields."""
    return MetaResponse(
        created_by=model.created_by,
        updated_by=model.updated_by,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def to_address_response(address: Address) -> AddressResponse:
    return AddressResponse(
        id=address.id,
        street_one=address.street_one,
        street_two=address.street_two,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country=address.country,
        meta=to_meta_response(address),
    )


def to_party_response(party: Party, address: Address) -> PartyResponse:
    return PartyResponse(
        id=party.id,
        first_name=party.first_name,
        middle_name=party.middle_name,
        last_name=party.last_name,
        email=party.email,
        phone_number=party.phone_number,
        address=to_address_response(address),
        meta=to_meta_response(party),
    )
