"""
API integration tests.
ultralytics is already mocked in conftest.py before these imports run.
"""

import io

from fastapi.testclient import TestClient
from PIL import Image

from main import app
from schemas import Detection

client = TestClient(app)


# ─── /health ──────────────────────────────────────────────────────────────────

def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_payload():
    response = client.get("/health")
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


# ─── /detectar/ — validation ──────────────────────────────────────────────────

def test_detect_non_image_returns_415():
    """PDF upload must be rejected with 415 Unsupported Media Type."""
    response = client.post(
        "/detectar/",
        files={"image_file": ("document.pdf", b"%PDF-1.4", "application/pdf")},
    )
    assert response.status_code == 415


def test_detect_plain_text_returns_415():
    response = client.post(
        "/detectar/",
        files={"image_file": ("note.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


# ─── /detectar/ — happy path ──────────────────────────────────────────────────

def _png_bytes() -> bytes:
    """Create a minimal valid PNG in memory."""
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), color=(128, 128, 128)).save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


def test_detect_image_returns_200_with_no_detections(monkeypatch):
    """When the detector finds nothing, the response is still 200 with an empty list."""
    import object_detector
    monkeypatch.setattr(object_detector.detector, "detect", lambda _: [])

    response = client.post(
        "/detectar/",
        files={"image_file": ("empty.png", _png_bytes(), "image/png")},
    )
    assert response.status_code == 200
    assert response.json() == {"detecciones": []}


def test_detect_image_returns_detections(monkeypatch):
    """Detections returned by the model are serialised correctly."""
    mock_detections = [
        Detection(objeto="person", confianza=0.92, coordenadas=[10.0, 20.0, 80.0, 160.0]),
        Detection(objeto="car", confianza=0.87, coordenadas=[0.0, 0.0, 64.0, 64.0]),
    ]

    import object_detector
    monkeypatch.setattr(object_detector.detector, "detect", lambda _: mock_detections)

    response = client.post(
        "/detectar/",
        files={"image_file": ("scene.png", _png_bytes(), "image/png")},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["detecciones"]) == 2
    assert body["detecciones"][0]["objeto"] == "person"
    assert body["detecciones"][1]["objeto"] == "car"
