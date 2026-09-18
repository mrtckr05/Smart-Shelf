from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Shelf
from app.schemas.shelf import ShelfCreate


def create_shelf(
    db: Session,
    shelf_data: ShelfCreate
) -> Shelf:

    shelf = Shelf(
        name=shelf_data.name
    )

    db.add(shelf)
    db.commit()
    db.refresh(shelf)

    return shelf


def get_shelves(db: Session) -> list[Shelf]:

    statement = select(Shelf)

    shelves = db.scalars(statement).all()

    return shelves