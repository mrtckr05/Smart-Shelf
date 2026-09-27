from app.services.yolo_service import yolo_service


IMAGE_PATH = "test_image.jpg"


results = yolo_service.detect(IMAGE_PATH)

counts = yolo_service.count_objects(results)

print("Detected objects:")
print(counts)