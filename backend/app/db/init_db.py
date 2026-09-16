from app.db.database import engine
from app.models.base import Base

from app.models import (
    Shelf,
    Product,
    Inventory,
    Observation,
    ObservedProduct,
)


def init_db():
    Base.metadata.create_all(bind=engine)