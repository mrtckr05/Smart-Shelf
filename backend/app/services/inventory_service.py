from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Inventory, Observation, Product
from app.schemas.inventory import InventoryCreate


def create_inventory(db: Session, inventory_data):

    inventory = Inventory(
        shelf_id=inventory_data.shelf_id,
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    statement = (
        select(
            Inventory,
            Product.name,
            Product.class_name
        )
        .join(
            Product,
            Inventory.product_id == Product.id
        )
        .where(
            Inventory.id == inventory.id
        )
    )

    row = db.execute(statement).one()

    inventory, name, class_name = row

    return {
        "id": inventory.id,
        "shelf_id": inventory.shelf_id,
        "product_id": inventory.product_id,
        "name": name,
        "class_name": class_name,
        "quantity": inventory.quantity
    }


def get_inventory(db: Session, shelf_id: int):

    statement = (
        select(
            Inventory,
            Product.name,
            Product.class_name
        )
        .join(
            Product,
            Inventory.product_id == Product.id
        )
        .where(
            Inventory.shelf_id == shelf_id
        )
    )

    rows = db.execute(statement).all()

    return [
        {
            "id": inventory.id,
            "shelf_id": inventory.shelf_id,
            "product_id": inventory.product_id,
            "name": name,
            "class_name": class_name,
            "quantity": inventory.quantity
        }
        for inventory, name, class_name in rows
    ]

def update_inventory_from_observation(
    db: Session,
    observation: Observation
) -> list[Inventory]:

    updated_inventory = []

    for observed_product in observation.products:

        statement = select(Inventory).where(
            Inventory.shelf_id == observation.shelf_id,
            Inventory.product_id == observed_product.product_id
        )

        inventory = db.scalar(statement)

        if inventory is None:

            inventory = Inventory(
                shelf_id=observation.shelf_id,
                product_id=observed_product.product_id,
                quantity=observed_product.quantity
            )

            db.add(inventory)

        else:

            inventory.quantity = observed_product.quantity

        updated_inventory.append(inventory)

    db.commit()

    for inventory in updated_inventory:
        db.refresh(inventory)

    return updated_inventory