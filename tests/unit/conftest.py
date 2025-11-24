from dataclasses import dataclass, asdict, field
from datetime import datetime
from src.dto.response_dtos import PartyResponse, AddressResponse, MetaResponse

import pytest


@dataclass
class TestMeta:
    createdBy: str = "test.user"
    createdAt: datetime = datetime.strptime("2025-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S")


@dataclass
class TestAddress:
    streetOne: str = "123 Main St"
    streetTwo: str = "Apt 4B"
    city: str = "Springfield"
    state: str = "IL"
    postalCode: str = "62704"
    country: str = "USA"
    meta: TestMeta = field(default_factory=TestMeta)


@dataclass
class TestParty:
    firstName: str = "John"
    middleName: str = "A."
    lastName: str = "Doe"
    email: str = "john.doe@example.com"
    phoneNumber: str = "5551234567"
    address: TestAddress = field(default_factory=TestAddress)
    meta: TestMeta = field(default_factory=TestMeta)


@pytest.fixture
def party_request() -> TestParty:
    return TestParty()


@pytest.fixture
def post_payload(party_request) -> dict:
    return asdict(party_request)


@pytest.fixture
def meta_response():
    test_meta = TestMeta()
    return MetaResponse(
        created_by=test_meta.createdBy,
        updated_by=test_meta.createdBy,
        created_at=test_meta.createdAt,
        updated_at=test_meta.createdAt,
    )


@pytest.fixture
def address_response(meta_response):
    test_address = TestAddress()
    return AddressResponse(
        id=1,
        street_one=test_address.streetOne,
        street_two=test_address.streetTwo,
        city=test_address.city,
        state=test_address.state,
        postal_code=test_address.postalCode,
        country=test_address.country,
        meta=meta_response,
    )


@pytest.fixture
def party_response(address_response, meta_response):
    test_party = TestParty()
    return PartyResponse(
        id=1,
        first_name=test_party.firstName,
        middle_name=test_party.middleName,
        last_name=test_party.lastName,
        email=test_party.email,
        phone_number=test_party.phoneNumber,
        address=address_response,
        meta=meta_response,
    )
