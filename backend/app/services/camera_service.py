import cv2


class CameraService:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        if self.cap is not None:
            return

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            raise RuntimeError(
                f"Kamera açılamadı: {self.camera_index}"
            )

    def read(self):
        if self.cap is None:
            self.start()

        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Kameradan görüntü alınamadı.")

        return frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None