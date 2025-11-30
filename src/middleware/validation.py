from functools import wraps
from typing import Type, TypeVar, Callable, Any
from flask import request
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
PartyResponseTuple = tuple[dict[str, Any], int]


def validate_request(
    model: Type[T],
) -> Callable[
    [Callable[[Any, T], PartyResponseTuple]], Callable[[Any], PartyResponseTuple]
]:
    """Returns a decorator that validates the request payload against the provided pydantic model."""

    def decorator(
        func: Callable[[Any, T], PartyResponseTuple],
    ) -> Callable[[Any], PartyResponseTuple]:
        @wraps(func)
        def wrapper(self: Any) -> PartyResponseTuple:
            logger.debug("Validating request.")
            return func(self, model(**request.json))

        return wrapper

    return decorator
