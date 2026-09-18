from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas.product import ProductCreate


def create_product(
    db: Session,
    product_data: ProductCreate
) -> Product:

    product = Product(
        name=product_data.name,
        class_name=product_data.class_name
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session) -> list[Product]:
    statement = select(Product)

    products = db.scalars(statement).all()

    return products