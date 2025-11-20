import hashlib
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from src.dto.custom_types import GeneralStringConstraint, PostalType
from src.config.enums import USState


class AddressDTO(BaseModel):
    """Validates the address information portion of the request payload"""

    model_config = ConfigDict(alias_generator=to_camel)

    street_one: GeneralStringConstraint
    street_two: Optional[GeneralStringConstraint] = None
    city: GeneralStringConstraint
    state: str = Field(min_length=2, max_length=2)
    postal_code: PostalType
    country: str = Field(min_length=3, max_length=3)
    id: Optional[int] = None

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
        for name in AddressDTO.model_fields.keys():
            val = getattr(self, name)
            if val:
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
