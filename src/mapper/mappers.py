from src.dto.address_dto import AddressDTO
from src.dto.party_dto import PartyDTO
from src.models.address import Address
from src.models.party import Party


def to_party_model(party_dto: PartyDTO) -> Party:
    party = Party()
    party.first_name = party_dto.first_name
    party.last_name = party_dto.last_name
    party.middle_name = party_dto.middle_name
    party.email = str(party_dto.email)
    party.phone_number = str(party_dto.phone_number)
    return party


def to_address_model(address_dto: AddressDTO) -> Address:
    address = Address()
    address.street_one = address_dto.street_one
    address.street_two = address_dto.street_two
    address.city = address_dto.city
    address.state = address_dto.state
    address.postal_code = address_dto.postal_code
    address.country = address_dto.country
    return address
