from ultralytics import YOLO
import cv2
import numpy as np
import io

class ObjectDetectionService:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')  # Utiliser le modèle nano pour commencer
        
    async def detect_objects(self, image_bytes):
        try:
            # Convertir les bytes en numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Faire la détection
            results = self.model(image)
            
            # Extraire les résultats
            detections = []
            for r in results:
                for box in r.boxes:
                    obj = {
                        "class": r.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()
                    }
                    detections.append(obj)
            
            return detections
            
        except Exception as e:
            raise Exception(f"Erreur lors de la détection d'objets: {str(e)}")
