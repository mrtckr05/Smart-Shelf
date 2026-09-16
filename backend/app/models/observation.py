from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.shelf import Shelf
    from app.models.observed_product import ObservedProduct


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)

    shelf_id: Mapped[int] = mapped_column(
        ForeignKey("shelves.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    shelf: Mapped["Shelf"] = relationship(
        back_populates="observations"
    )

    products: Mapped[list["ObservedProduct"]] = relationship(
        back_populates="observation",
        cascade="all, delete-orphan"
    )