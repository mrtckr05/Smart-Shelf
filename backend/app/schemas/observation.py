from datetime import datetime

from pydantic import BaseModel, Field


class ObservedProductCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=0)


class ObservationCreate(BaseModel):
    shelf_id: int
    products: list[ObservedProductCreate]


class ObservedProductResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }


class ObservationResponse(BaseModel):
    id: int
    shelf_id: int
    created_at: datetime
    products: list[ObservedProductResponse]

    model_config = {
        "from_attributes": True
    }