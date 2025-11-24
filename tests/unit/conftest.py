from dataclasses import dataclass, asdict, field
from datetime import datetime
from src.dto.response_dtos import PartyResponse, AddressResponse, MetaResponse
import pytest
from src.service.party_service import PartyService
from src.models import Party, Address, PartyHistory


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
def test_party() -> TestParty:
    return TestParty()


@pytest.fixture
def post_payload(test_party) -> dict:
    return asdict(test_party)


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


@pytest.fixture
def mock_uow(mocker):
    """Mock Unit of Work with all repositories"""
    uow = mocker.MagicMock()
    uow.party_repository = mocker.MagicMock()
    uow.address_repository = mocker.MagicMock()
    uow.party_history_repository = mocker.MagicMock()
    uow.__enter__ = mocker.MagicMock(return_value=None)
    uow.__exit__ = mocker.MagicMock(return_value=True)
    return uow


@pytest.fixture
def mock_cache_repository(mocker):
    return mocker.MagicMock()


@pytest.fixture
def party_service(mock_uow, mock_cache_repository):
    return PartyService(mock_uow, mock_cache_repository)


@pytest.fixture
def mock_address(mocker, test_party):
    address = mocker.MagicMock(spec=Address)
    address.id = 1
    address.street_one = test_party.address.streetOne
    address.street_two = test_party.address.streetTwo
    address.city = test_party.address.city
    address.state = test_party.address.state
    address.postal_code = test_party.address.postalCode
    address.country = test_party.address.country
    return address


@pytest.fixture
def mock_party(mocker, test_party):
    party = mocker.MagicMock(spec=Party)
    party.id = 1
    party.first_name = test_party.firstName
    party.middle_name = test_party.middleName
    party.last_name = test_party.lastName
    party.email = test_party.email
    party.phone_number = test_party.phoneNumber
    return party


@pytest.fixture
def mock_party_history(mocker):
    history = mocker.MagicMock(spec=PartyHistory)
    history.id = 1
    history.party_id = 1
    return history


@pytest.fixture
def mock_mappers(mocker):
    return mocker.patch("src.service.party_service.mappers")
