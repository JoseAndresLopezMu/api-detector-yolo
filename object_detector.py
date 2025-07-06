from ultralytics import YOLO
from PIL import Image
import io
from config import settings
from schemas import Detection

class ObjectDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image_bytes: bytes) -> list[Detection]:
        image = Image.open(io.BytesIO(image_bytes))
        results = self.model(image)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if class_id in settings.CLASSES_OF_INTEREST and confidence >= settings.MODEL_CONFIDENCE:
                    detections.append(
                        Detection(
                            objeto=self.model.names[class_id],
                            confianza=round(confidence, 2),
                            coordenadas=box.xyxy[0].tolist()
                        )
                    )
        return detections

detector = ObjectDetector(model_path=settings.MODEL_PATH)
