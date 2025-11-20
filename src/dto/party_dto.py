from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel

from src.dto.address_dto import AddressDTO
from src.dto.custom_types import GeneralStringConstraint, PhoneType
from src.dto.meta_dto import MetaDTO


class PartyDTO(BaseModel):
    """Validates the personal information portion of the request payload"""

    model_config = ConfigDict(alias_generator=to_camel)
    first_name: GeneralStringConstraint
    middle_name: Optional[GeneralStringConstraint] = None
    last_name: GeneralStringConstraint
    email: EmailStr
    phone_number: PhoneType
    address: AddressDTO
    meta: MetaDTO
    id: Optional[int] = None
