from redis import Redis
from pydantic import BaseModel
import logging
from typing import TYPE_CHECKING
from src.config.constants import AppConstants
from src.config.enums import ServiceEntities

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from typing import Awaitable


class CacheRepository:
    def __init__(self, cache: Redis) -> None:
        self._cache = cache

    def add(self, id: int, entity: ServiceEntities, value: BaseModel) -> None:
        bytes_val = value.model_dump_json().encode("utf-8")
        self._cache.set(
            self._generate_key(id, entity), bytes_val
        )  # TODO: expiration time
        logger.info(f"Party with ID {id} saved in cache.")

    def get(self, id: int, entity: ServiceEntities) -> Awaitable[bytes]:
        return self._cache.get(self._generate_key(id, entity))

    @staticmethod
    def _generate_key(id: int, entity: ServiceEntities) -> str:
        return f"{AppConstants.APP_NAME}:{entity.value}:{id}"
