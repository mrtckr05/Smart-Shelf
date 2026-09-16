from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.inventory import Inventory
    from app.models.observed_product import ObservedProduct


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    class_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    inventory: Mapped[list["Inventory"]] = relationship(
        back_populates="product"
    )

    observations: Mapped[list["ObservedProduct"]] = relationship(
        back_populates="product"
    )