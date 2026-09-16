from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import BASE_DIR


DATA_DIR = BASE_DIR / "backend" / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'smartshelf.db'}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()