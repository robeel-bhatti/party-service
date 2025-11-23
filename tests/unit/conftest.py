from dataclasses import dataclass, asdict, field
from datetime import datetime

import pytest


@dataclass
class TestMeta:
    createdBy: str = "test.user"
    createdAt: datetime = datetime.now()


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
