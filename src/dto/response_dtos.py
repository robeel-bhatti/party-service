from datetime import datetime


class MetaResponse:
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime


class AddressResponse:
    street_one: str
    street_two: str | None = None
    city: str
    state: str
    postal_code: str
    country: str
    meta: MetaResponse


class PartyResponse:
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    phone_number: str
    address: AddressResponse
    meta: MetaResponse
