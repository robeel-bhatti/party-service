from src.dto.request_dtos import PartyRequest, AddressRequest
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory


def to_party(party_request: PartyRequest) -> Party:
    party = Party()
    party.first_name = party_request.first_name
    party.last_name = party_request.last_name
    party.middle_name = party_request.middle_name
    party.email = str(party_request.email)
    party.phone_number = str(party_request.phone_number)
    party.created_by = party_request.meta.created_by
    party.updated_by = party_request.meta.created_by
    return party


def to_address(address_request: AddressRequest) -> Address:
    address = Address()
    address.street_one = address_request.street_one
    address.street_two = address_request.street_two
    address.city = address_request.city
    address.state = address_request.state
    address.postal_code = address_request.postal_code
    address.country = address_request.country
    address.created_by = address_request.meta.created_by
    address.updated_by = address_request.meta.created_by
    address.hash = address_request.get_hash()
    return address


def to_party_history(party: Party, address: Address) -> PartyHistory:
    party_history = PartyHistory()
    party_history.party_id = party.id
    party_history.first_name = party.first_name
    party_history.last_name = party.last_name
    party_history.middle_name = party.middle_name
    party_history.email = party.email
    party_history.phone_number = party.phone_number
    party_history.party_created_at = party.created_at
    party_history.party_updated_at = party.updated_at
    party_history.party_created_by = party.created_by
    party_history.party_updated_by = party.updated_by
    party_history.street_one = address.street_one
    party_history.street_two = address.street_two
    party_history.city = address.city
    party_history.state = address.state
    party_history.zip_code = address.postal_code
    party_history.country = address.country
    return party_history
