import asyncio

import cv2

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from app.services.camera_manager import CameraManager


router = APIRouter()

camera_manager = CameraManager(camera_index=0)


async def generate_frames():

    while True:

        frame = camera_manager.get_latest_frame()

        if frame is None:
            await asyncio.sleep(0.1)
            continue

        success, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )

        await asyncio.sleep(0.05)


@router.get("/stream")
async def camera_stream():

    camera_manager.start()

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.websocket("/ws")
async def camera_websocket(websocket: WebSocket):

    await websocket.accept()

    camera_manager.start()

    try:

        while True:

            counts = camera_manager.get_latest_counts()

            await websocket.send_json({
                "counts": counts
            })

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:

        print("Camera WebSocket bağlantısı kapandı.")