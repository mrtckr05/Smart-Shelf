from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Inventory
from app.schemas.inventory import InventoryCreate


def create_inventory(
    db: Session,
    inventory_data: InventoryCreate
) -> Inventory:

    inventory = Inventory(
        shelf_id=inventory_data.shelf_id,
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory


def get_inventory(
    db: Session,
    shelf_id: int
) -> list[Inventory]:

    statement = select(Inventory).where(
        Inventory.shelf_id == shelf_id
    )

    inventory = db.scalars(statement).all()

    return inventory