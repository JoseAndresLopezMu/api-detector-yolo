import io

import gradio as gr
from PIL import Image, ImageDraw

from object_detector import detector


def _color(label: str) -> str:
    return "#FF4B4B" if label == "person" else "#4B9CFF"


def predict(pil_image: Image.Image):
    if pil_image is None:
        return None, "Sube una imagen para comenzar."

    buf = io.BytesIO()
    pil_image.save(buf, format="JPEG")
    detections = detector.detect(buf.getvalue())

    # Draw bounding boxes on a copy of the image
    annotated = pil_image.copy()
    draw = ImageDraw.Draw(annotated)

    for det in detections:
        x1, y1, x2, y2 = det.coordenadas
        color = _color(det.objeto)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        label = f" {det.objeto}  {det.confianza:.0%} "
        text_w = len(label) * 7
        draw.rectangle([x1, y1 - 20, x1 + text_w, y1], fill=color)
        draw.text((x1 + 2, y1 - 18), label, fill="white")

    # Build summary text
    if not detections:
        summary = "No se detectaron personas ni coches en la imagen."
    else:
        persons = sum(1 for d in detections if d.objeto == "person")
        cars = sum(1 for d in detections if d.objeto == "car")
        lines = []
        if persons:
            lines.append(f"Personas detectadas:  {persons}")
        if cars:
            lines.append(f"Coches detectados:    {cars}")
        lines.append("")
        for det in detections:
            lines.append(f"• {det.objeto.capitalize()} — confianza {det.confianza:.0%}")
        summary = "\n".join(lines)

    return annotated, summary


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="Imagen de entrada"),
    outputs=[
        gr.Image(type="pil", label="Resultado"),
        gr.Textbox(label="Detecciones", lines=5),
    ],
    title="Detector de Personas y Coches — YOLOv10",
    description=(
        "Sube una imagen para detectar **personas** (rojo) y **coches** (azul) "
        "en tiempo real usando YOLOv10n."
    ),
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
