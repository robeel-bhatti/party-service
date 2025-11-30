import hashlib

from datetime import datetime
from typing import Optional, Self, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
from pydantic import Field, model_validator
from src.util.enums import USState

# Custom types to be reused against fields belonging in multiple pydantic models.
GeneralStringConstraint = Annotated[
    str, Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9\s\-\.']+$")
]
PhoneType = Annotated[str, Field(min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$")]
PostalType = Annotated[
    str, Field(min_length=1, max_length=10, pattern=r"^\d{5}(-\d{4})?$")
]


class MetaRequest(BaseModel):
    """Validates the metadata information in the request payload."""

    model_config = ConfigDict(alias_generator=to_camel)
    created_by: GeneralStringConstraint
    created_at: datetime


class AddressRequest(BaseModel):
    """Validates the address information portion of the request payload"""

    model_config = ConfigDict(alias_generator=to_camel)

    street_one: GeneralStringConstraint
    street_two: Optional[GeneralStringConstraint] = None
    city: GeneralStringConstraint
    state: str = Field(min_length=2, max_length=2)
    postal_code: PostalType
    country: str = Field(min_length=3, max_length=3)
    meta: MetaRequest

    @model_validator(mode="after")
    def parse_state(self) -> Self:
        try:
            USState(self.state.upper())
        except ValueError:
            raise ValueError(
                f"Failed to create Party. An invalid US state code: '{self.state}' was provided."
            )
        return self

    @model_validator(mode="after")
    def normalize_fields(self) -> Self:
        for name in AddressRequest.model_fields.keys():
            val = getattr(self, name)
            if val and name != "meta":
                val = val.strip()
                if name == "state" or name == "country":
                    val = val.upper()
                elif name == "city":
                    val = val.capitalize()
                elif name == "street_one" or name == "street_two":
                    val = val.title()

            setattr(self, name, val)

        return self

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


class PartyRequest(BaseModel):
    """Validates the personal information portion of the request payload"""

    model_config = ConfigDict(alias_generator=to_camel)
    first_name: GeneralStringConstraint
    middle_name: Optional[GeneralStringConstraint] = None
    last_name: GeneralStringConstraint
    email: EmailStr
    phone_number: PhoneType
    address: AddressRequest
    meta: MetaRequest
