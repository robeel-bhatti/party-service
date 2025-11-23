from redis import Redis
import logging
import json
from typing import Awaitable, Any
from src.config.constants import AppConstants
from src.config.enums import ServiceEntities

logger = logging.getLogger(__name__)


class CacheRepository:
    """Responsible for interacting with the external Cache being used by this application for faster reads."""

    def __init__(self, cache: Redis) -> None:
        self._cache = cache

    def add(self, id: int, entity: ServiceEntities, value: Any) -> None:
        """
        Add an entity to the cache.
        :param id: The unique identifier (ex. primary key) for the entity.
        :param entity: An enum identifying the entity being stored.
        :param value: The attributes of the entity.
        """
        bytes_val = json.dumps(value).encode("utf-8")
        self._cache.set(self._generate_key(id, entity), bytes_val, ex=86400)

    def get(self, id: int, entity: ServiceEntities) -> Awaitable[bytes]:
        """
        Get an entity from the cache.
        :param id: The unique identifier (ex. primary key) for the entity.
        :param entity: An enum identifying the entity being stored.
        :return: The attributes of the entity.
        """
        return self._cache.get(self._generate_key(id, entity))

    @staticmethod
    def _generate_key(id: int, entity: ServiceEntities) -> str:
        """
        Generate a unique cache key for the entity. The creation of this cache key
        allows the cache to create a namespace or "folder" that belongs only to this service.
        :param id: The unique identifier (ex. primary key) for the entity.
        :param entity: An enum identifying the entity being stored.
        :return: A unique cache key.
        """
        return f"{AppConstants.APP_NAME}:{entity.value}:{id}"
