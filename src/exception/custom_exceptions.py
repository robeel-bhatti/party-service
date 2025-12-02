from dataclasses import asdict, dataclass
from typing import Any, Self

from src.util.enums import ServiceEntities


@dataclass(frozen=True)
class ErrorDTO:
    """
    Custom DTO that represents the error response payload.
    This uses the Problem-Details error message format -> https://www.rfc-editor.org/rfc/rfc9457.html"""

    status: int
    title: str
    detail: str
    instance: str
    type: str = "about:blank"

    def to_dict(self: Self, **extensions: Any) -> dict[str, Any]:
        """Convert an instance to a dictionary.
        If there are extra fields that need to be in the error response payload they can be passed in via keyword arguments.
        """
        err_dict = asdict(self)
        err_dict.update(extensions)
        return err_dict


class EntityNotFound(Exception):
    def __init__(self, entity_name: ServiceEntities, entity_id: int) -> None:
        self.entity_name = entity_name.value.capitalize()
        self.entity_id = entity_id
        super().__init__(f"{self.entity_name} with ID {entity_id} was not found.")
