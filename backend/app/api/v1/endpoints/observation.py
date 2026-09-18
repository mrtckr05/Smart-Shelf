from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.observation import (
    ObservationCreate,
    ObservationResponse
)
from app.services.observation_service import (
    create_observation,
    get_observation,
    get_shelf_observations
)


router = APIRouter()


@router.post(
    "/",
    response_model=ObservationResponse
)
def create_observation_endpoint(
    observation_data: ObservationCreate,
    db: Session = Depends(get_db)
):
    return create_observation(db, observation_data)


@router.get(
    "/{observation_id}",
    response_model=ObservationResponse
)
def get_observation_endpoint(
    observation_id: int,
    db: Session = Depends(get_db)
):
    return get_observation(db, observation_id)


@router.get(
    "/shelf/{shelf_id}",
    response_model=list[ObservationResponse]
)
def get_shelf_observations_endpoint(
    shelf_id: int,
    db: Session = Depends(get_db)
):
    return get_shelf_observations(db, shelf_id)