from dataclasses import dataclass, asdict, field
from datetime import datetime
from src.dto.response_dtos import PartyResponse, AddressResponse, MetaResponse
import pytest
from src.service.party_service import PartyService
from src.models import Party, Address, PartyHistory
from src.dto.request_dtos import PartyRequest


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
def default_party_data() -> TestParty:
    return TestParty()


@pytest.fixture
def default_address_data() -> TestAddress:
    return TestAddress()


@pytest.fixture
def default_meta_data() -> TestMeta:
    return TestMeta()


@pytest.fixture
def post_payload(default_party_data) -> dict:
    return asdict(default_party_data)


@pytest.fixture
def party_request(post_payload):
    return PartyRequest(**post_payload)


@pytest.fixture
def meta_response(default_meta_data):
    return MetaResponse(
        created_by=default_meta_data.createdBy,
        updated_by=default_meta_data.createdBy,
        created_at=default_meta_data.createdAt,
        updated_at=default_meta_data.createdAt,
    )


@pytest.fixture
def address_response(default_address_data, meta_response):
    return AddressResponse(
        id=1,
        street_one=default_address_data.streetOne,
        street_two=default_address_data.streetTwo,
        city=default_address_data.city,
        state=default_address_data.state,
        postal_code=default_address_data.postalCode,
        country=default_address_data.country,
        meta=meta_response,
    )


@pytest.fixture
def party_response(default_party_data, address_response, meta_response):
    return PartyResponse(
        id=1,
        first_name=default_party_data.firstName,
        middle_name=default_party_data.middleName,
        last_name=default_party_data.lastName,
        email=default_party_data.email,
        phone_number=default_party_data.phoneNumber,
        address=address_response,
        meta=meta_response,
    )


@pytest.fixture
def party_fixture(default_party_data):
    party = Party()
    party.id = 1
    party.first_name = default_party_data.firstName
    party.middle_name = default_party_data.middleName
    party.last_name = default_party_data.lastName
    party.email = default_party_data.email
    party.phone_number = default_party_data.phoneNumber
    return party


@pytest.fixture
def address_fixture(default_party_data):
    address = Address()
    address.id = 1
    address.street_one = default_party_data.address.streetOne
    address.street_two = default_party_data.address.streetTwo
    address.city = default_party_data.address.city
    address.state = default_party_data.address.state
    address.postal_code = default_party_data.address.postalCode
    address.country = default_party_data.address.country
    return address


@pytest.fixture
def party_history_fixture():
    history = PartyHistory()
    history.id = 1
    history.party_id = 1
    return history


@pytest.fixture
def party_service(mock_uow, mock_cache_repository):
    return PartyService(mock_uow, mock_cache_repository)


@pytest.fixture
def mock_uow(mocker):
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
def mock_mappers(mocker):
    return mocker.patch("src.service.party_service.mappers")
