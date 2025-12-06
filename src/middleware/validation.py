from functools import wraps
from typing import TypeVar, ParamSpec, Type, Callable
from flask import request
from pydantic import BaseModel
import logging
from src.util.custom_types import PartyResponseTuple

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
P = ParamSpec("P")


def validate_request(
    model: Type[T],
) -> Callable[[Callable[..., PartyResponseTuple]], Callable[P, PartyResponseTuple]]:
    """Returns a decorator that validates the request payload against the provided pydantic model."""

    def decorator(
        func: Callable[..., PartyResponseTuple],
    ) -> Callable[P, PartyResponseTuple]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> PartyResponseTuple:
            logger.debug("Validating request.")
            return func(*args, model(**request.json), **kwargs)

        return wrapper

    return decorator
