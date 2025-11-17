from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.address import Address
    from src.models.party_history import PartyHistory


class Party(Base):
    """Party table model"""

    __tablename__ = "party"
    __table_args__ = {"schema": "party_service"}

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(10))
    address_id: Mapped[int] = mapped_column(ForeignKey("party_service.address.id"))
    address: Mapped["Address"] = relationship(back_populates="parties")
    history_records: Mapped[List["PartyHistory"]] = relationship(back_populates="party")
