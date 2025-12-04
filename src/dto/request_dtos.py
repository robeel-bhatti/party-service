from datetime import datetime
from typing import Annotated, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
from pydantic import Field, AfterValidator

from src.util.enums import USState
import hashlib


def postal_code_validator(postal_code: str) -> str | None:
    return postal_code.strip() if postal_code else None


def street_city_validator(value: str) -> str | None:
    return value.strip().title() if value else None


def country_validator(country: str) -> str | None:
    return country.strip().upper() if country else None


def state_validator(state: str) -> str | None:
    if state is None:
        return None
    new_state = state.strip().upper()
    try:
        USState(new_state)
    except ValueError:
        raise ValueError(
            f"Failed to create Party. An invalid US state code: '{state}' was provided."
        )
    return new_state


# Custom types to be reused against fields belonging in multiple pydantic models.
GeneralStringType = Annotated[
    str, Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9\s\-\.']+$")
]
PhoneType = Annotated[str, Field(min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$")]
GeneralAddressType = Annotated[
    str,
    Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9\s\-\.']+$"),
    AfterValidator(street_city_validator),
]
StateType = Annotated[
    str, Field(min_length=2, max_length=2), AfterValidator(state_validator)
]
PostalType = Annotated[
    str,
    Field(min_length=1, max_length=10, pattern=r"^\d{5}(-\d{4})?$"),
    AfterValidator(postal_code_validator),
]
CountryType = Annotated[
    str, Field(min_length=3, max_length=3), AfterValidator(country_validator)
]


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class MetaCreate(CustomBaseModel):
    created_by: GeneralStringType
    created_at: datetime


class MetaUpdate(CustomBaseModel):
    updated_by: GeneralStringType
    updated_at: datetime


class AddressHashMixin:
    if TYPE_CHECKING:
        street_one: str | None
        street_two: str | None
        city: str | None
        state: str | None
        postal_code: str | None
        country: str | None

    def get_hash(self) -> str:
        """Normalize address components, then get a deterministic hash."""
        normalized_string = (
            f"{self.street_one}"
            f"|{self.street_two if self.street_two else ''}"
            f"|{self.city}"
            f"|{self.state}"
            f"|{self.postal_code}"
            f"|{self.country}"
        )
        return hashlib.sha256(normalized_string.encode()).hexdigest()


class AddressCreate(CustomBaseModel, AddressHashMixin):
    street_one: GeneralAddressType
    street_two: GeneralAddressType | None = None
    city: GeneralAddressType
    state: StateType
    postal_code: PostalType
    country: CountryType


class AddressUpdate(CustomBaseModel, AddressHashMixin):
    street_one: GeneralAddressType | None = None
    street_two: GeneralAddressType | None = None
    city: GeneralAddressType | None = None
    state: StateType | None = None
    postal_code: PostalType | None = None
    country: CountryType | None = None


class PartyCreate(CustomBaseModel):
    first_name: GeneralStringType
    middle_name: GeneralStringType | None = None
    last_name: GeneralStringType
    email: EmailStr
    phone_number: PhoneType
    address: AddressCreate
    meta: MetaCreate


class PartyUpdate(CustomBaseModel):
    """
    Meta UpdatedBy is used in the following situations during a PATCH request:
    1. Party row in TBL_PARTY when Party attribute is updated
    2. Party row in TBL_PARTY when Party address is updated
    3. Address row in TBL_ADDRESS when a new Address is created.
    """

    first_name: GeneralStringType | None = None
    middle_name: GeneralStringType | None = None
    last_name: GeneralStringType | None = None
    email: EmailStr | None = None
    phone_number: PhoneType | None = None
    address: AddressUpdate | None = None
    meta: MetaUpdate
