from typing import Optional, Self

from custom_types import GeneralStringConstraint, PostalType
from pydantic import BaseModel, Field, model_validator

from src.enums.state_enum import USState


class AddressDTO(BaseModel):
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
            raise ValueError(f"Invalid US state code: {self.state}")
        return self
