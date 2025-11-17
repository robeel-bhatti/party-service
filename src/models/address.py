from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.party import Party


class Address(Base):
    """Represents a row from party_service.address

    This table stores address information.
    """

    __tablename__ = "address"
    __table_args__ = {"schema": "party_service"}

    id: Mapped[int] = mapped_column(primary_key=True)
    street_one: Mapped[str] = mapped_column(String(50))
    street_two: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(2))
    postal_code: Mapped[str] = mapped_column(String(10))
    country: Mapped[str] = mapped_column(String(3))
    hash: Mapped[str] = mapped_column(Text)
    parties: Mapped[List["Party"]] = relationship(back_populates="address")
