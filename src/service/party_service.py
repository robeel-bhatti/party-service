from src.repository.unit_of_work import UnitOfWork


class PartyService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work

    def add_party(self) -> None:
        with self.uow:
            pass
