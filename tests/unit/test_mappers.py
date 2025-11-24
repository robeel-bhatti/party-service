from src.mapper import mappers
from src.dto.request_dtos import PartyRequest
from src.models.party import Party
from src.models.address import Address
from src.models.party_history import PartyHistory


def test_to_party(test_party, post_payload):
    """Test that all fields are correctly mapped from PartyRequest to Party"""
    party_request = PartyRequest(**post_payload)
    result = mappers.to_party(party_request)

    assert isinstance(result, Party)
    assert result.first_name == test_party.firstName
    assert result.middle_name == test_party.middleName
    assert result.last_name == test_party.lastName
    assert result.email == test_party.email
    assert result.phone_number == test_party.phoneNumber
    assert result.created_by == test_party.meta.createdBy
    assert result.updated_by == test_party.meta.createdBy
    assert result.updated_by == result.created_by


def test_to_address(test_party, post_payload):
    """Test that all fields are correctly mapped from AddressRequest to Address"""
    party_request = PartyRequest(**post_payload)
    address_request = party_request.address
    result = mappers.to_address(address_request)

    assert isinstance(result, Address)
    assert result.street_one == test_party.address.streetOne
    assert result.street_two == test_party.address.streetTwo
    assert result.city == test_party.address.city
    assert result.state == test_party.address.state
    assert result.postal_code == test_party.address.postalCode
    assert result.country == test_party.address.country
    assert result.created_by == test_party.address.meta.createdBy
    assert result.updated_by == test_party.address.meta.createdBy
    assert result.updated_by == result.created_by


def test_to_party_history(test_party, mock_party, mock_address):
    """Test that Party and Address are mapping correctly to PartyHistory"""
    result = mappers.to_party_history(mock_party, mock_address)

    assert isinstance(result, PartyHistory)
    assert result.party_id == mock_party.id
    assert result.first_name == test_party.firstName
    assert result.middle_name == test_party.middleName
    assert result.last_name == test_party.lastName
    assert result.email == test_party.email
    assert result.phone_number == test_party.phoneNumber
