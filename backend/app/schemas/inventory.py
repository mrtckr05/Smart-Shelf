from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    shelf_id: int
    product_id: int
    quantity: int = Field(ge=0)


class InventoryResponse(BaseModel):
    id: int
    shelf_id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }