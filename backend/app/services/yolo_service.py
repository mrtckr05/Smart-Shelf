import cv2
from app.core.config import settings
import json




class YOLOService:
    def __init__(self, model_path : str):
        self.model_path = model_path

    def load_model(self):
        # YOLO modelini yükle
        pass

    def preprocess_image(self, image):
        # Görüntüyü model için ön işleme tabi tut
        pass

    def detect_objects(self, image):
        # Görüntüde nesne tespiti yap
        pass

    def draw_boxes(self, image, detections):
        # Tespit edilen nesnelerin etrafına kutular çiz
        pass

    def process_image(self, image_path):
        # Görüntüyü yükle
        image = cv2.imread(image_path)
        
        # Nesne tespiti yap
        detections = self.detect_objects(image)
        
        # Kutuları çiz
        self.draw_boxes(image, detections)
        
        return image, detections

    def save_image(self, image, output_path):
        # Görüntüyü kaydet
        cv2.imwrite(output_path, image)
        
