import logging
from types import TracebackType

from sqlalchemy.orm import Session

from src.models.address import Address
from src.models.party import Party
from src.repository.abstract_repository import AbstractRepository

uow_logger = logging.getLogger(__name__)


class UnitOfWork:
    """This class will manage transactions across multiple repositories"""

    def __init__(
        self,
        session: Session,
        party_repository: AbstractRepository[Party],
        address_repository: AbstractRepository[Address],
    ):
        self.session = session
        self.party_repository = party_repository
        self.address_repository = address_repository

    def __enter__(self) -> None:
        uow_logger.info("Starting Transaction...")

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if exc_type:
            self.session.rollback()
            return False

        self.session.commit()
        return None
