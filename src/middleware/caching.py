from functools import wraps
from typing import Callable, Any
import logging
from redis import RedisError
from src.util.enums import ServiceEntities
from flask.globals import current_app
from src.util.custom_types import PartyResponseTuple

logger = logging.getLogger(__name__)


def cache_read(
    entity_type: ServiceEntities,
) -> Callable[
    [Callable[[Any, int], PartyResponseTuple]], Callable[[Any, int], PartyResponseTuple]
]:
    """Returns a decorator that checks the cache for an entity via the provided ID."""

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
