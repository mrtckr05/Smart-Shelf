Smart-Shelf/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI application, CORS, and lifespan
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py            # v1 router aggregator
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── detection.py  # Detection endpoints
│   │   │           └── shelf.py      # Shelf endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py             # Pydantic Settings configuration
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # SQLAlchemy engine and session
│   │   │   └── init_db.py            # Database table initialization
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── inventory.py
│   │   │   ├── observation.py
│   │   │   ├── observed_product.py
│   │   │   ├── product.py
│   │   │   └── shelf.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── detection.py
│   │   │   └── shelf.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── yolo_service.py       # Image processing and YOLO service scaffold
│   ├── data/                         # Local SQLite database (excluded from Git)
│   ├── create_db.py                  # Database initialization script
│   ├── Dockerfile
│   └── requirements.txt
├── .gitignore
├── docker-compose.yml
├── folder_structure.md
└── README.md