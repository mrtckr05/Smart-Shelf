from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Observation, ObservedProduct
from app.schemas.observation import ObservationCreate


def create_observation(
    db: Session,
    observation_data: ObservationCreate
) -> Observation:

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

def get_observation(
    db: Session,
    observation_id: int
) -> Observation | None:

    statement = select(Observation).where(
        Observation.id == observation_id
    )

    return db.scalar(statement)

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