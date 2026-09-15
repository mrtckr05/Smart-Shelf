from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartShelf API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Frontend (Next.js) bağlantısı için CORS izinleri
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Model ağırlık yolu
    MODEL_PATH: str = ""

    class Config:
        case_sensitive = True

settings = Settings()