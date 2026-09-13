from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings

# Sunucu başlarken ve kapanırken çalışacak Lifespan fonksiyonu
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Başlangıç: Model yükleme veya DB bağlantıları burada başlatılır
    print(f"🚀 {settings.PROJECT_NAME} başlatılıyor...")
    yield
    # Kapanış: Kaynakları temizleme
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

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME, "version": settings.VERSION}