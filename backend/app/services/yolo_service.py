from pathlib import Path
from collections import Counter

from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "weights" / "best.pt"


class YOLOService:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect(self, source):
        return self.model(source)

    def count_objects(self, results):
        counts = Counter()

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]

                counts[class_name] += 1

        return dict(counts)


yolo_service = YOLOService()