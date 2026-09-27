import asyncio

import cv2

from app.services.yolo_service import yolo_service


class CameraManager:

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index

        self.cap = None
        self.latest_frame = None
        self.latest_counts = {}

        self.running = False
        self.task = None

    def start(self):
        if self.running:
            return

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None

            raise RuntimeError(
                f"Kamera açılamadı: {self.camera_index}"
            )

        self.running = True
        self.task = asyncio.create_task(
            self._camera_loop()
        )

    async def _camera_loop(self):

        while self.running:

            try:
                success, frame = await asyncio.to_thread(
                    self.cap.read
                )

                if not success:
                    print("Kameradan görüntü alınamadı.")
                    await asyncio.sleep(1)
                    continue

                results = await asyncio.to_thread(
                    yolo_service.detect,
                    frame
                )

                counts = yolo_service.count_objects(results)

                annotated_frame = results[0].plot()

                self.latest_frame = annotated_frame
                self.latest_counts = counts

                await asyncio.sleep(0.05)

            except Exception as e:
                print(f"Camera loop error: {e}")
                await asyncio.sleep(1)

    def get_latest_frame(self):
        return self.latest_frame

    def get_latest_counts(self):
        return self.latest_counts

    async def stop(self):

        self.running = False

        if self.task is not None:
            await self.task
            self.task = None

        if self.cap is not None:
            self.cap.release()
            self.cap = None