import pytest

from src.dto.request_dtos import PartyRequest, AddressRequest


def test_party_request_created_successfully(post_payload: dict, party_request):
    party_dto = PartyRequest(**post_payload)
    assert party_dto is not None
    assert isinstance(party_dto, PartyRequest)
    assert party_dto.first_name == party_request.firstName
    assert party_dto.middle_name == party_request.middleName
    assert party_dto.last_name == party_request.lastName
    assert party_dto.phone_number == party_request.phoneNumber
    assert party_dto.email == party_request.email
    assert party_dto.address is not None
    assert isinstance(party_dto.address, AddressRequest)
    assert party_dto.address.street_one == party_request.address.streetOne
    assert party_dto.address.street_two == party_request.address.streetTwo
    assert party_dto.address.city == party_request.address.city
    assert party_dto.address.state == party_request.address.state
    assert party_dto.address.postal_code == party_request.address.postalCode
    assert party_dto.address.country == party_request.address.country


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
