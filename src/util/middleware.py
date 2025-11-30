from functools import wraps
from typing import Type, TypeVar, Callable, Any, ParamSpec
from flask import request
from pydantic import BaseModel
import logging
from redis import RedisError
from src.config.enums import ServiceEntities
from flask.globals import current_app

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
R = TypeVar("R")
P = ParamSpec("P")
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


def cache_read(
    entity_type: ServiceEntities,
) -> Callable[
    [Callable[[Any, int], PartyResponseTuple]], Callable[[Any, int], PartyResponseTuple]
]:
    def decorator(
        func: Callable[[Any, int], PartyResponseTuple],
    ) -> Callable[[Any, int], PartyResponseTuple]:
        @wraps(func)
        def wrapper(self: Any, id: int) -> PartyResponseTuple:
            entity = entity_type.value
            cache_repo = current_app.container.cache_repository
            logger.debug(f"Getting {entity} with ID: {id} from cache.")
            cached = None

            try:
                cached = cache_repo.get(id, entity_type)
            except RedisError as e:
                logger.warning(
                    f"Could not get {entity} with ID {id} due to Redis Error: {e}"
                )
            if cached:
                logger.debug(f"Cache hit for {entity} with ID {id}.")
                return cached, 200
            logger.debug(f"Cache miss for {entity} with ID {id}.")
            return func(self, id)

        return wrapper

    return decorator
