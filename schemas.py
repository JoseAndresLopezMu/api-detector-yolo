from pydantic import BaseModel
from typing import List

class Detection(BaseModel):
    """Define la estructura de una única detección."""
    objeto: str
    confianza: float
    coordenadas: List[float]

class DetectionResponse(BaseModel):
    """Define la estructura de la respuesta de la API."""
    detecciones: List[Detection]