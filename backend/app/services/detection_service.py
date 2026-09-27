from app.services.yolo_service import yolo_service
from app.services.observation_service import (
    create_observation_from_counts
)


def detect_and_count(image_path: str):
    results = yolo_service.detect(image_path)
    counts = yolo_service.count_objects(results)

    return counts