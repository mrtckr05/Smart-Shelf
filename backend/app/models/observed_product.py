from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.observation import Observation
    from app.models.product import Product


class ObservedProduct(Base):
    __tablename__ = "observed_products"

    id: Mapped[int] = mapped_column(primary_key=True)

    observation_id: Mapped[int] = mapped_column(
        ForeignKey("observations.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    observation: Mapped["Observation"] = relationship(
        back_populates="products"
    )

    product: Mapped["Product"] = relationship(
        back_populates="observations"
    )