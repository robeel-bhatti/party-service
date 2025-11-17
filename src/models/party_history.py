from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.party import Party


class PartyHistory(Base):
    """Represents a row from party_service.party_history
    This table stores historical versions of party records."""

    __tablename__ = "party_history"
    __table_args__ = {"schema": "party_service"}

    id: Mapped[int] = mapped_column(primary_key=True)
    party_id: Mapped[int] = mapped_column(ForeignKey("party_service.party.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(10))
    street_one: Mapped[str] = mapped_column(String(50))
    street_two: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(2))
    zip_code: Mapped[str] = mapped_column(String(10))
    country: Mapped[str] = mapped_column(String(3))
    party_created_at: Mapped[datetime]
    party_updated_at: Mapped[datetime]
    party_created_by: Mapped[str] = mapped_column(String(50))
    party_updated_by: Mapped[str] = mapped_column(String(50))
    party: Mapped["Party"] = relationship(back_populates="history_records")
