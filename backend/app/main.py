from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.app.api.zone import router as zones_router
from backend.app.modules.camera_service import CameraService

import asyncio
import cv2
import time


# ============================================================
# ARGUS API
# ============================================================

app = FastAPI(
    title="Argus API",
    version="0.1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CAMERA SERVICE
# ============================================================

camera_service = CameraService()


app.state.camera_service = camera_service


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(zones_router)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():

    print("Starting Argus Camera Service...")

    camera_service.start()


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
def shutdown():

    print("Stopping Argus Camera Service...")

    camera_service.stop()


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "name": "Argus",
        "status": "online"
    }


# ============================================================
# CAMERA STATUS
# ============================================================

@app.get("/api/camera/status")
def camera_status():

    return camera_service.get_status()


# ============================================================
# VIDEO FRAME GENERATOR
# ============================================================

def generate_frames():

    while True:

        frame = camera_service.get_frame()

        if frame is None:

            time.sleep(0.01)

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

        time.sleep(0.01)


# ============================================================
# LIVE CAMERA STREAM
# ============================================================

@app.get("/api/camera/stream")
def camera_stream():

    return StreamingResponse(
        generate_frames(),
        media_type=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        )
    )


# ============================================================
# ARGUS EVENT WEBSOCKET
# ============================================================

@app.websocket("/ws/events")
async def events_websocket(
    websocket: WebSocket
):

    await websocket.accept()

    print(
        "Argus event client connected."
    )

    try:

        while True:

            events = camera_service.get_events()

            for event in events:

                event_data = (
                    camera_service.event_to_dict(
                        event
                    )
                )

                await websocket.send_json(
                    event_data
                )

            await asyncio.sleep(0.1)

    except Exception:

        print(
            "Argus event client disconnected."
        )