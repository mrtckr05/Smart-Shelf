smartshelf/
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI instance, CORS ve Lifespan (Model yükleme)
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # v1 router birleştirici
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── detection.py # YOLO inference endpoint'leri (/detect, /track vb.)
│   │           └── shelf.py     # Raf doluluk, stok ve sayım CRUD/analiz endpoint'leri
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Pydantic Settings (.env, model path, CORS ayarları)
│   ├── models/                  # (Opsiyonel) DB modelleri (SQLAlchemy / Tortoise)
│   │   └── __init__.py
│   ├── schemas/                 # Pydantic Request/Response modelleri
│   │   ├── __init__.py
│   │   ├── detection.py         # Bounding box, confidence, sınıf çıktı şemaları
│   │   └── shelf.py             # Raf durumu, ürün şemaları
│   ├── services/                # İş mantığı ve AI Pipeline
│   │   ├── __init__.py
│   │   └── yolo_service.py      # Ultralytics/YOLO model wrapper (singleton/cached)
│   └── weights/                 # Model ağırlık dosyaları (.pt, .onnx)
│       └── best.pt
├── requirements.txt
└── Dockerfile
├── frontend/                # Next.js + TypeScript
│   ├── src/
│   ├── Dockerfile           # (opsiyonel)
│   └── package.json
├── .github/
│   └── workflows/
│       ├── ci.yml           # lint + test
│       └── deploy.yml       # Docker build + deploy
├── docker-compose.yml       # Local geliştirme için
├── README.md
└── ml/
    ├── data/                 # Eğitim ve test veri setleri
    ├── src/                  # Eğitim ve değerlendirme scriptleri            