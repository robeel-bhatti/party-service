from typing import Optional, Self

from address_dto import AddressDTO
from custom_types import GeneralStringConstraint, PhoneType
from pydantic import BaseModel, EmailStr, model_validator


class PartyDTO(BaseModel):
    first_name: GeneralStringConstraint
    middle_name: Optional[GeneralStringConstraint] = None
    last_name: Optional[GeneralStringConstraint] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneType] = None
    address: AddressDTO

    @model_validator(mode="after")
    def check_fields(self) -> Self:
        if self.email is None and self.phone_number is None:
            raise ValueError("Either `email` or `phone_number` must be provided")
        return self
