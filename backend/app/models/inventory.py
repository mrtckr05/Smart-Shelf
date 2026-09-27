from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.shelf import Shelf
    from app.models.product import Product


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
    UniqueConstraint(
        "shelf_id",
        "product_id",
        name="uq_inventory_shelf_product"
    ),
)

    id: Mapped[int] = mapped_column(primary_key=True)

    shelf_id: Mapped[int] = mapped_column(
        ForeignKey("shelves.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )

    shelf: Mapped["Shelf"] = relationship(
        back_populates="inventory"
    )

    product: Mapped["Product"] = relationship(
        back_populates="inventory"
    )