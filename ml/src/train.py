from ultralytics import YOLO
import mlflow
from pathlib import Path

# Bu dosyanın (scriptin) bulunduğu klasörün yolunu otomatik alır
BASE_DIR = Path(__file__).resolve().parent

# Verisetinin yolunu buna göre oluşturur
DATASET_PATH = BASE_DIR / "dataset.yaml"


MODEL_NAME = "yolo11n.pt"

EPOCHS = 50
IMAGE_SIZE = 640
BATCH_SIZE = 16
DEVICE = 0

PROJECT_NAME = "smartshelf"
RUN_NAME = "yolo11n_baseline"


def main():

    # MLflow
    mlflow.set_experiment("SmartShelf")

    # Model
    model = YOLO(MODEL_NAME)

    # Training
    results = model.train(
        data=DATASET_PATH,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        device=DEVICE,

        project=PROJECT_NAME,
        name=RUN_NAME,

        pretrained=True,
        seed=42,
        save=True,
        patience=10,

        # Windows multiprocessing problemi için
        workers=0,
    )

    # Validation
    metrics = model.val(
        data=DATASET_PATH,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        device=DEVICE,
        workers=0,
    )

    print("\n=== Final Validation Results ===")

    print(f"Precision : {metrics.box.mp:.4f}")
    print(f"Recall    : {metrics.box.mr:.4f}")
    print(f"mAP50     : {metrics.box.map50:.4f}")
    print(f"mAP50-95  : {metrics.box.map:.4f}")


if __name__ == "__main__":
    main()