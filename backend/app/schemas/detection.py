from pydantic import BaseModel


class DetectionResponse(BaseModel):
    counts: dict[str, int]