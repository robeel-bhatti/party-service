from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from pydantic.alias_generators import to_camel

from src.dto.address_dto import AddressDTO
from src.dto.custom_types import GeneralStringConstraint, PhoneType


class PartyDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    first_name: GeneralStringConstraint
    middle_name: Optional[GeneralStringConstraint] = None
    last_name: Optional[GeneralStringConstraint] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneType] = None
    address: AddressDTO

    @model_validator(mode="after")
    def check_fields(self) -> Self:
        if self.email is None and self.phone_number is None:
            raise ValueError(
                "Failed to create Party. Either email or phone_number must be provided."
            )
        return self
