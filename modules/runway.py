from ultralytics import YOLO
from PIL import Image
import numpy as np

MODEL_PATH = "models/runway_best.pt"

# Load runway model once
model = YOLO(MODEL_PATH)


def analyze_runway(image):
    """
    Detect runway in an input image.

    Returns:
        annotated_image: image with runway bounding box
        detections: list of detected runways
        runway_detected: True/False
    """

    image_array = np.array(image)

    results = model.predict(
        source=image_array,
        conf=0.25,
        verbose=False
    )

    result = results[0]

    detections = []

    if result.boxes is not None:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

    return {
        "annotated_image": result.plot(),
        "detections": detections,
        "runway_detected": len(detections) > 0
    }