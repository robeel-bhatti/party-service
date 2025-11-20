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
        """
        When an instance of this class starts being used as a context manager, this magic method
        will be invoked. This will start the database transaction.
        :return:
        """
        uow_logger.info("Starting Transaction...")

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """
        When an instance of this class stops being used as a context manager, this magic method
        will be invoked. This will stop the database transaction by either committing or rolling back.
        :param exc_type: The exception type, if an exception occurs.
        :param exc_val: The exception value, if an exception occurs.
        :param exc_tb: The exception traceback, if an exception occurs.
        :return:
        """
        if exc_type:
            print("Rolling back Transaction...")
            self.session.rollback()
            return False

        self.session.commit()
        return None

    def flush(self) -> None:
        """
        Flush all object changes in the current transaction. This will allow us to retrieve the state of the entity
        of how it will be persisted in the database, before we actually commit. Useful for getting the IDs of entities.
        """
        self.session.flush()
