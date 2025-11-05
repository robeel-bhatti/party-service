from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from src.dto.custom_types import GeneralStringConstraint, PostalType
from src.enums.state_enum import USState


class AddressDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    street_one: GeneralStringConstraint
    street_two: Optional[GeneralStringConstraint] = None
    city: GeneralStringConstraint
    state: str = Field(min_length=2, max_length=2)
    postal_code: PostalType
    country: str = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def parse_state(self) -> Self:
        try:
            USState(self.state)
        except ValueError:
            raise ValueError(
                f"Failed to create Party. An invalid US state code: '{self.state}' was provided."
            )
        return self
