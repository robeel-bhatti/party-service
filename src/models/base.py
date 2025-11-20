from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class with common audit fields

    Should be inherited by all other SQLAlchemy models.
    """

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[str] = mapped_column(String(50))
    updated_by: Mapped[str] = mapped_column(String(50))
