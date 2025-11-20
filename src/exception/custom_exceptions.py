from dataclasses import asdict, dataclass
from typing import Any, Self


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
