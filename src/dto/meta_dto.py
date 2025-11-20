from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.dto.custom_types import GeneralStringConstraint


class MetaDTO(BaseModel):
    """Validates the metadata information in the request payload."""

    model_config = ConfigDict(alias_generator=to_camel)
    created_by: GeneralStringConstraint
