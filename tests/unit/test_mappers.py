from src.util import mappers
from src.dto.request_dtos import PartyCreate
from src.models.party import Party
from src.models.address import Address
from src.models.party_history import PartyHistory


def test_to_party(default_party_data, post_payload):
    """Test that all fields are correctly mapped from PartyRequest to Party"""
    party_request = PartyCreate(**post_payload)
    result = mappers.to_party(party_request)

    assert isinstance(result, Party)
    assert result.first_name == default_party_data.firstName
    assert result.middle_name == default_party_data.middleName
    assert result.last_name == default_party_data.lastName
    assert result.email == default_party_data.email
    assert result.phone_number == default_party_data.phoneNumber
    assert result.created_by == default_party_data.meta.createdBy
    assert result.updated_by == default_party_data.meta.createdBy
    assert result.updated_by == result.created_by


def test_to_address(default_party_data, post_payload):
    """Test that all fields are correctly mapped from AddressRequest to Address"""
    party_request = PartyCreate(**post_payload)
    address_request = party_request.address
    result = mappers.to_address(address_request)

    assert isinstance(result, Address)
    assert result.street_one == default_party_data.address.streetOne
    assert result.street_two == default_party_data.address.streetTwo
    assert result.city == default_party_data.address.city
    assert result.state == default_party_data.address.state
    assert result.postal_code == default_party_data.address.postalCode
    assert result.country == default_party_data.address.country


def test_to_party_history(default_party_data, party_fixture, address_fixture):
    """Test that Party and Address are mapping correctly to PartyHistory"""
    result = mappers.to_party_history(party_fixture)

    assert isinstance(result, PartyHistory)
    assert result.party_id == party_fixture.id
    assert result.first_name == default_party_data.firstName
    assert result.middle_name == default_party_data.middleName
    assert result.last_name == default_party_data.lastName
    assert result.email == default_party_data.email
    assert result.phone_number == default_party_data.phoneNumber
