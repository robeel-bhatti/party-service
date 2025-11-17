from redis import Redis


class CacheRepository:
    def __init__(self, cache: Redis) -> None:
        self.cache = cache
