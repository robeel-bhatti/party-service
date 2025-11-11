import hashlib
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel

from src.dto.address_dto import AddressDTO
from src.dto.custom_types import GeneralStringConstraint, PhoneType
from src.dto.meta_dto import MetaDTO


class PartyDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    first_name: GeneralStringConstraint
    middle_name: Optional[GeneralStringConstraint] = None
    last_name: GeneralStringConstraint
    email: EmailStr
    phone_number: PhoneType
    address: AddressDTO
    meta: MetaDTO
    id: Optional[int] = None

    def get_hash(self) -> str:
        """Normalize party components, then get a deterministic hash."""
        normalized_string = (
            f"{self.first_name} "
            f"|{self.middle_name if self.middle_name else ''}"
            f"|{self.last_name}"
            f"|{self.email}"
            f"|{self.phone_number}"
        )
        return hashlib.sha256(normalized_string.encode()).hexdigest()
