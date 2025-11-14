# from sqlalchemy.orm import Session
# from sqlalchemy.sql import select
# from typing import TypeVar, Generic
# from src.models.base import Base
#
# T = TypeVar("T")
#
#
# class BaseRepository(Generic[T]):
#     def __init__(self, session: Session) -> None:
#         self.session = session
#
#     def add(self, entity: T) -> None:
#         self.session.add(entity)
#
#     def get_by_hash(self, entity: T, hash: str) -> Base | None:
#         return self.session.execute(select(entity).where(entity.hash == hash)).scalar()
