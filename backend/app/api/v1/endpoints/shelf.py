from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.shelf import ShelfCreate, ShelfResponse
from app.services.shelf_service import (
    create_shelf,
    get_shelves
)


router = APIRouter()


@router.post(
    "/",
    response_model=ShelfResponse
)
def create_shelf_endpoint(
    shelf_data: ShelfCreate,
    db: Session = Depends(get_db)
):
    return create_shelf(db, shelf_data)


@router.get(
    "/",
    response_model=list[ShelfResponse]
)
def get_shelves_endpoint(
    db: Session = Depends(get_db)
):
    return get_shelves(db)