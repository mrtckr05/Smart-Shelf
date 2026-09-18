from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse
)
from app.services.inventory_service import (
    create_inventory,
    get_inventory
)


router = APIRouter()


@router.post(
    "/",
    response_model=InventoryResponse
)
def create_inventory_endpoint(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db)
):
    return create_inventory(db, inventory_data)


@router.get(
    "/shelf/{shelf_id}",
    response_model=list[InventoryResponse]
)
def get_shelf_inventory_endpoint(
    shelf_id: int,
    db: Session = Depends(get_db)
):
    return get_inventory(db, shelf_id)