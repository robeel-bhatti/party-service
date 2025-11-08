from dataclasses import asdict, dataclass
from typing import Any, Self


@dataclass(frozen=True)
class ErrorDTO:
    """Problem-Details error message format -> https://www.rfc-editor.org/rfc/rfc9457.html"""

    status: int
    title: str
    detail: str
    instance: str
    type: str = "about:blank"

    def to_dict(self: Self, **extensions: Any) -> dict[str, Any]:
        err_dict = asdict(self)
        err_dict.update(extensions)
        return err_dict
