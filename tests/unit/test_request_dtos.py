import pytest

from src.dto.request_dtos import PartyRequest, AddressRequest


def test_party_request_created_successfully(post_payload: dict, default_party_data):
    party_dto = PartyRequest(**post_payload)
    assert party_dto is not None
    assert isinstance(party_dto, PartyRequest)
    assert party_dto.first_name == default_party_data.firstName
    assert party_dto.middle_name == default_party_data.middleName
    assert party_dto.last_name == default_party_data.lastName
    assert party_dto.phone_number == default_party_data.phoneNumber
    assert party_dto.email == default_party_data.email
    assert party_dto.address is not None
    assert isinstance(party_dto.address, AddressRequest)
    assert party_dto.address.street_one == default_party_data.address.streetOne
    assert party_dto.address.street_two == default_party_data.address.streetTwo
    assert party_dto.address.city == default_party_data.address.city
    assert party_dto.address.state == default_party_data.address.state
    assert party_dto.address.postal_code == default_party_data.address.postalCode
    assert party_dto.address.country == default_party_data.address.country


def test_throws_error_when_invalid_state_is_provided(post_payload: dict):
    post_payload["address"]["state"] = "XY"
    with pytest.raises(ValueError) as err:
        PartyRequest(**post_payload)
    assert "invalid US state code" in str(err.value)


def test_fields_are_normalized(post_payload: dict):
    post_payload["address"]["city"] = "richmond "
    post_payload["address"]["state"] = "va"
    post_payload["address"]["postalCode"] = "12345"
    post_payload["address"]["country"] = "usa"
    post_payload["address"]["streetOne"] = "123 main street"
    post_payload["address"]["streetTwo"] = "suite 45 "
    party = PartyRequest(**post_payload)
    assert party.address.city == "Richmond"
    assert party.address.state == "VA"
    assert party.address.postal_code == "12345"
    assert party.address.country == "USA"
    assert party.address.street_one == "123 Main Street"
    assert party.address.street_two == "Suite 45"


def test_address_dto_hash(post_payload: dict):
    """Ensure hashing method returns deterministic output"""
    party = PartyRequest(**post_payload)
    hash_one = party.address.get_hash()
    hash_two = party.address.get_hash()
    assert hash_one == hash_two
