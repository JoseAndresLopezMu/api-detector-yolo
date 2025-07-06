import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from object_detector import detector
from schemas import DetectionResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="API de Detección de Objetos con YOLOv10",
    description="Una API para detectar objetos (personas y coches) en imágenes usando YOLOv10.",
    version="1.0.0"
)

@app.post("/detectar/", response_model=DetectionResponse)
async def detectar_objetos(image_file: UploadFile = File(...)):
    if not image_file.content_type.startswith("image/"):
        logging.warning(f"Intento de subida de archivo no soportado: {image_file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="El archivo proporcionado no es una imagen."
        )

    try:
        logging.info(f"Procesando el archivo: {image_file.filename}")
        contents = await image_file.read()
        
        detections = detector.detect(contents)
        
        logging.info(f"Detección completada. Se encontraron {len(detections)} objetos.")
        return {"detecciones": detections}

    except Exception:
        logging.exception("Ocurrió un error inesperado al procesar la imagen.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al procesar la imagen."
        )
