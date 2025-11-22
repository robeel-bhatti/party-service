import pytest

from src.dto.address_dto import AddressRequest
from src.dto.request_dtos import PartyRequest
from tests.unit.conftest import TEST_ADDRESS, TEST_USER


def test_party_and_address_dto_are_created_successfully(post_payload: dict):
    party_dto = PartyRequest(**post_payload)
    assert party_dto is not None
    assert isinstance(party_dto, PartyRequest)
    assert party_dto.first_name == TEST_USER.first_name
    assert party_dto.middle_name == TEST_USER.middle_name
    assert party_dto.last_name == TEST_USER.last_name
    assert party_dto.phone_number == TEST_USER.phone_number
    assert party_dto.email == TEST_USER.email
    assert party_dto.address is not None
    assert isinstance(party_dto.address, AddressRequest)
    assert party_dto.address.street_one == TEST_ADDRESS.street_one
    assert party_dto.address.street_two == TEST_ADDRESS.street_two
    assert party_dto.address.city == TEST_ADDRESS.city
    assert party_dto.address.state == TEST_ADDRESS.state
    assert party_dto.address.postal_code == TEST_ADDRESS.postal_code
    assert party_dto.address.country == TEST_ADDRESS.country


def test_throws_error_when_email_and_phone_number_are_missing(post_payload: dict):
    post_payload["email"] = None
    post_payload["phoneNumber"] = None
    with pytest.raises(ValueError) as err:
        PartyRequest(**post_payload)
    assert "email or phone_number must be provided" in str(err.value)


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
