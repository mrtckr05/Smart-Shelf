from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.inventory import Inventory
    from app.models.observation import Observation


class Shelf(Base):
    __tablename__ = "shelves"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    inventory: Mapped[list["Inventory"]] = relationship(
        back_populates="shelf"
    )

    observations: Mapped[list["Observation"]] = relationship(
        back_populates="shelf"
    )