from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Self, Any


def make_json_serializable(data: list[tuple[str, Any]]) -> dict[str, Any]:
    """
    The custom dictionary factory function that returns a JSON-serializable object in order to be cached
    and set over the wire.
    This function takes in a list of tuples, which each tuple containing the dataclass field, and the respective value.

    Any fields whose value is an instance of the datetime class is converted to a string representing UTC time.
    All fields are converted to camel case.
    """

    def convert_value(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def to_camel_case(snake_str: str) -> str:
        """Convert snake_case string to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(word.capitalize() for word in components[1:])

    return {to_camel_case(k): convert_value(v) for k, v in data}


@dataclass
class MetaResponse:
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime


@dataclass
class AddressResponse:
    id: int
    street_one: str
    city: str
    state: str
    postal_code: str
    country: str
    meta: MetaResponse
    street_two: str | None = None


@dataclass
class PartyResponse:
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: AddressResponse
    meta: MetaResponse
    middle_name: str | None = None

    def to_dict(self: Self) -> dict[str, Any]:
        """Convert an instance of this dataclass to a JSON-serializable dictionary"""
        return asdict(self, dict_factory=make_json_serializable)
