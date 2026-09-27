from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Observation,
    ObservedProduct,
    Shelf,
    Product
)
from app.schemas.observation import ObservationCreate


from app.services.inventory_service import (
    update_inventory_from_observation
)


def create_observation(
    db: Session,
    observation_data: ObservationCreate
) -> Observation:

    # Shelf kontrolü
    shelf = db.scalar(
        select(Shelf).where(
            Shelf.id == observation_data.shelf_id
        )
    )

    if shelf is None:
        raise HTTPException(
            status_code=404,
            detail="Shelf bulunamadı."
        )

    # Product kontrolü
    for product_data in observation_data.products:

        product = db.scalar(
            select(Product).where(
                Product.id == product_data.product_id
            )
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {product_data.product_id} bulunamadı."
            )

    # Observation oluştur
    observation = Observation(
        shelf_id=observation_data.shelf_id
    )

    for product_data in observation_data.products:

        observed_product = ObservedProduct(
            product_id=product_data.product_id,
            quantity=product_data.quantity
        )

        observation.products.append(observed_product)

    db.add(observation)
    db.commit()
    db.refresh(observation)


    return observation

def create_observation_from_counts(
    db: Session,
    shelf_id: int,
    counts: dict[str, int]
) -> Observation:

    products = []

    for class_name, quantity in counts.items():

        statement = select(Product).where(
            Product.class_name == class_name
        )

        product = db.scalar(statement)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product bulunamadı: {class_name}"
            )

        products.append({
            "product_id": product.id,
            "quantity": quantity
        })

    observation_data = ObservationCreate(
        shelf_id=shelf_id,
        products=products
    )

    return create_observation(
        db,
        observation_data
    )


def get_observation(
    db: Session,
    observation_id: int
) -> Observation:

    statement = select(Observation).where(
        Observation.id == observation_id
    )

    observation = db.scalar(statement)

    if observation is None:
        raise HTTPException(
            status_code=404,
            detail="Observation bulunamadı."
        )

    return observation

def get_shelf_observations(
    db: Session,
    shelf_id: int
) -> list[Observation]:

    statement = (
        select(Observation)
        .where(Observation.shelf_id == shelf_id)
        .order_by(Observation.created_at.desc())
    )

    return list(db.scalars(statement).all())