from app.services.camera_service import CameraService
from app.services.yolo_service import yolo_service


class CameraDetectionService:

    def __init__(self, camera_index: int = 0):
        self.camera = CameraService(camera_index)

    def detect_frame(self):
        frame = self.camera.read()

        results = yolo_service.detect(frame)
        counts = yolo_service.count_objects(results)

        annotated_frame = results[0].plot()

        return annotated_frame, counts

    def stop(self):
        self.camera.stop()