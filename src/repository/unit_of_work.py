import logging
from types import TracebackType

from sqlalchemy.orm import Session

from src.repository.party_history_repository import PartyHistoryRepository
from src.repository.address_repository import AddressRepository
from src.repository.party_repository import PartyRepository

uow_logger = logging.getLogger(__name__)


class UnitOfWork:
    """The class will manage transactions across multiple repositories.

    This avoids the need to handle transactions using multiple repositories.
    """

    def __init__(
        self,
        session: Session,
        party_repository: PartyRepository,
        address_repository: AddressRepository,
        party_history_repository: PartyHistoryRepository,
    ):
        self.session = session
        self.party_repository = party_repository
        self.address_repository = address_repository
        self.party_history_repository = party_history_repository

    def __enter__(self) -> None:
        uow_logger.info("Starting Transaction...")

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if exc_type:
            print("Rolling back Transaction...")
            self.session.rollback()
            return False

        self.session.commit()
        return None

    def flush(self) -> None:
        self.session.flush()
