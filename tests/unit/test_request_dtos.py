import pytest

from src.dto.request_dtos import PartyCreate, AddressCreate, PartyUpdate


def test_party_create_dto_created_successfully(post_payload: dict, default_party_data):
    party_dto = PartyCreate(**post_payload)
    assert party_dto is not None
    assert isinstance(party_dto, PartyCreate)
    assert party_dto.first_name == default_party_data.firstName
    assert party_dto.middle_name == default_party_data.middleName
    assert party_dto.last_name == default_party_data.lastName
    assert party_dto.phone_number == default_party_data.phoneNumber
    assert party_dto.email == default_party_data.email
    assert party_dto.address is not None
    assert isinstance(party_dto.address, AddressCreate)
    assert party_dto.address.street_one == default_party_data.address.streetOne
    assert party_dto.address.street_two == default_party_data.address.streetTwo
    assert party_dto.address.city == default_party_data.address.city
    assert party_dto.address.state == default_party_data.address.state
    assert party_dto.address.postal_code == default_party_data.address.postalCode
    assert party_dto.address.country == default_party_data.address.country


def test_throws_error_when_invalid_state_is_provided(post_payload: dict):
    post_payload["address"]["state"] = "xy"
    with pytest.raises(ValueError) as err:
        PartyCreate(**post_payload)
    assert "invalid US state code" in str(err.value)


def test_fields_are_normalized(post_payload: dict):
    post_payload["address"]["city"] = "richmond "
    post_payload["address"]["state"] = "va"
    post_payload["address"]["postalCode"] = "12345"
    post_payload["address"]["country"] = "usa"
    post_payload["address"]["streetOne"] = "123 main street"
    post_payload["address"]["streetTwo"] = "suite 45 "
    party = PartyCreate(**post_payload)
    assert party.address.city == "Richmond"
    assert party.address.state == "VA"
    assert party.address.postal_code == "12345"
    assert party.address.country == "USA"
    assert party.address.street_one == "123 Main Street"
    assert party.address.street_two == "Suite 45"


def test_party_update_dto_created_successfully(patch_payload: dict):
    dto = PartyUpdate(**patch_payload)
    party = dto.model_dump(exclude_unset=True)

    assert party["first_name"] == "Jane"
    assert party["email"] == "jane.new@example.com"
    assert party["middle_name"] is None

    assert "last_name" not in party
    assert "phone_number" not in party

    assert "address" in party
    assert party["address"]["city"] == "New Town"
    assert party["address"]["state"] == "CA"

    assert "street_one" not in party["address"]
    assert "street_two" not in party["address"]
    assert "postal_code" not in party["address"]
    assert "country" not in party["address"]

    assert party["meta"]["updated_by"] == "patch.user"
    assert str(party["meta"]["updated_at"]) == "2025-01-02 10:00:00"
