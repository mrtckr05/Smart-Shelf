from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.schemas.detection import DetectionResponse
from app.services.detection_service import detect_and_count

router = APIRouter()


@router.post(
    "/image",
    response_model=DetectionResponse
)
async def detect_image(
    file: UploadFile = File(...)
):
    temp_path = Path("temp_" + file.filename)

    contents = await file.read()

    with open(temp_path, "wb") as buffer:
        buffer.write(contents)

    try:
        counts = detect_and_count(str(temp_path))

        return {
            "counts": counts
        }

    finally:
        if temp_path.exists():
            temp_path.unlink()