from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    class_name: str


class ProductResponse(BaseModel):
    id: int
    name: str
    class_name: str

    model_config = {
        "from_attributes": True
    }