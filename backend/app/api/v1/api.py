from fastapi import APIRouter

from app.api.v1.endpoints import detection
from app.api.v1.endpoints import shelf
from app.api.v1.endpoints import product
from app.api.v1.endpoints import inventory
from app.api.v1.endpoints import observation

api_router = APIRouter()


api_router.include_router(
    detection.router,
    prefix="/detection",
    tags=["Detection"]
)

api_router.include_router(
    shelf.router,
    prefix="/shelf",
    tags=["Shelf"]
)

api_router.include_router(
    product.router,
    prefix="/products",
    tags=["Products"]
)

api_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"]
)

api_router.include_router(
    observation.router,
    prefix="/observations",
    tags=["Observations"]
)