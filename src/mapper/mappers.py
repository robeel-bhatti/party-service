from src.dto.address_dto import AddressRequest
from src.dto.request_dtos import PartyRequest
from src.models.address import Address
from src.models.party import Party
from src.models.party_history import PartyHistory


def to_party_model(party_dto: PartyRequest) -> Party:
    party = Party()
    party.first_name = party_dto.first_name
    party.last_name = party_dto.last_name
    party.middle_name = party_dto.middle_name
    party.email = str(party_dto.email)
    party.phone_number = str(party_dto.phone_number)
    return party


def to_address_model(address_dto: AddressRequest) -> Address:
    address = Address()
    address.street_one = address_dto.street_one
    address.street_two = address_dto.street_two
    address.city = address_dto.city
    address.state = address_dto.state
    address.postal_code = address_dto.postal_code
    address.country = address_dto.country
    return address


def to_party_history_model(party: Party, address: Address) -> PartyHistory:
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
