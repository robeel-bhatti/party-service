from dataclasses import dataclass

import pytest


@dataclass
class TestUser:
    first_name: str = "John"
    middle_name: str = "A."
    last_name: str = "Doe"
    email: str = "john.doe@example.com"
    phone_number: str = "5551234567"


@dataclass
class TestAddress:
    street_one: str = "123 Main St"
    street_two: str = "Apt 4B"
    city: str = "Springfield"
    state: str = "IL"
    postal_code: str = "62704"
    country: str = "USA"


TEST_USER = TestUser()
TEST_ADDRESS = TestAddress()


@pytest.fixture
def post_payload() -> dict:
    return {
        "firstName": TEST_USER.first_name,
        "middleName": TEST_USER.middle_name,
        "lastName": TEST_USER.last_name,
        "email": TEST_USER.email,
        "phoneNumber": TEST_USER.phone_number,
        "address": {
            "streetOne": TEST_ADDRESS.street_one,
            "streetTwo": TEST_ADDRESS.street_two,
            "city": TEST_ADDRESS.city,
            "state": TEST_ADDRESS.state,
            "postalCode": TEST_ADDRESS.postal_code,
            "country": TEST_ADDRESS.country,
        },
    }
