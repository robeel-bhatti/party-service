from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Class to be inherited by all repositories.

    Contains shared methods that are used or can potentially be used by all repos.
    Only such methods should go in here.
    """

    def __init__(self, session: Session, clazz: Type[T]) -> None:
        self.session = session
        self.clazz = clazz

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def get_by_id(self, id: int) -> T:
        return self.session.get_one(entity=self.clazz, ident=id)
