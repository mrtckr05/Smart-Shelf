from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import (
    create_product,
    get_products
)


router = APIRouter()


@router.post(
    "/",
    response_model=ProductResponse
)
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product_data)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products_endpoint(
    db: Session = Depends(get_db)
):
    return get_products(db)