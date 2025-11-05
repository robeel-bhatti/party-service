from typing import Annotated

from pydantic import Field

GeneralStringConstraint = Annotated[
    str, Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9\s\-\.']+$")
]
PhoneType = Annotated[str, Field(min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$")]
PostalType = Annotated[
    str, Field(min_length=1, max_length=200, pattern=r"^\d{5}(-\d{4})?$")
]
