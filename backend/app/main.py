from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.services.camera_manager import CameraManager
from app.services.monitoring_service import MonitoringService


camera_manager = CameraManager(
    camera_index=settings.CAMERA_INDEX
)

monitoring_service = MonitoringService(
    camera_manager=camera_manager,
    shelf_id=settings.SHELF_ID
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Sunucu başlarken
    print(
        f"🚀 {settings.PROJECT_NAME} başlatılıyor..."
    )

    if settings.MONITORING_ENABLED:
        print("📷 Camera monitoring başlatılıyor...")

        camera_manager.start()
        monitoring_service.start()

    yield

    # Sunucu kapanırken
    if settings.MONITORING_ENABLED:
        print("🛑 Camera monitoring durduruluyor...")

        await monitoring_service.stop()
        await camera_manager.stop()

    print("🛑 Sunucu kapatılıyor...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


# Next.js erişimi için CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API router
app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/health", tags=["Health"])
def health_check():

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }