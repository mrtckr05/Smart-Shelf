from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent

# Dataset yolu
DATASET_PATH = BASE_DIR / "dataset.yaml"




SPLITS = ["train", "valid", "test"]

CLASS_NAMES = {
    0: "book",
    1: "pen",
    2: "cup",
    3: "toy_car",
}

image_extensions = {".jpg", ".jpeg", ".png", ".webp"}

total_images = 0
total_labels = 0
class_counts = Counter()

print("=== SmartShelf Dataset Check ===\n")

for split in SPLITS:
    image_dir = DATASET_DIR / split / "images"
    label_dir = DATASET_DIR / split / "labels"

    images = [
        p for p in image_dir.iterdir()
        if p.suffix.lower() in image_extensions
    ]

    labels = list(label_dir.glob("*.txt"))

    image_stems = {p.stem for p in images}
    label_stems = {p.stem for p in labels}

    missing_labels = image_stems - label_stems
    missing_images = label_stems - image_stems

    total_images += len(images)
    total_labels += len(labels)

    print(f"--- {split.upper()} ---")
    print(f"Images : {len(images)}")
    print(f"Labels : {len(labels)}")

    if missing_labels:
        print(f"UYARI: {len(missing_labels)} image için label yok.")

    if missing_images:
        print(f"UYARI: {len(missing_images)} label için image yok.")

    # Label içeriklerini kontrol et
    invalid_labels = 0

    for label_file in labels:
        with open(label_file, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                parts = line.strip().split()

                if not parts:
                    continue

                if len(parts) != 5:
                    print(f"BAD: {label_file} -> {line.strip()}")
                    invalid_labels += 1
                    continue

                class_id = int(parts[0])
                values = list(map(float, parts[1:]))

                if class_id not in CLASS_NAMES:
                    print(
                        f"UYARI: Geçersiz class ID "
                        f"{class_id} -> {label_file}"
                    )

                if not all(0 <= value <= 1 for value in values):
                    print(
                        f"UYARI: Koordinat 0-1 aralığında değil -> "
                        f"{label_file}:{line_number}"
                    )

                class_counts[class_id] += 1

    if invalid_labels:
        print(f"UYARI: {invalid_labels} hatalı annotation satırı.")

    print()

print("=== Genel Sonuç ===")
print(f"Toplam image : {total_images}")
print(f"Toplam label : {total_labels}")

print("\n=== Class Distribution ===")

for class_id, class_name in CLASS_NAMES.items():
    print(
        f"{class_id} -> {class_name:8s}: "
        f"{class_counts[class_id]}"
    )