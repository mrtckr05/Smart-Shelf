from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


def _find_project_root() -> Path:
    current_path = Path(__file__).resolve()
    root_markers = (".git", "folder_structure.md", "docker-compose.yml")

    for candidate in (current_path.parent, *current_path.parents):
        if any((candidate / marker).exists() for marker in root_markers):
            return candidate

    return current_path.parents[3]


BASE_DIR = _find_project_root()


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
    MODEL_PATH: str = str("")

    class Config:
        case_sensitive = True

settings = Settings()