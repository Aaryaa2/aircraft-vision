from ultralytics import YOLO
from PIL import Image
import numpy as np


# Load the trained Member 3 model
MODEL_PATH = "models/final_best.pt"

model = YOLO(MODEL_PATH)


def analyze_damage(image):
    """
    Analyze an aircraft image for surface damage.

    Detects:
    - corrosion
    - crack
    - dent
    """

    # Convert PIL image to numpy array
    image_array = np.array(image)

    # Run YOLO prediction
    results = model.predict(
        source=image_array,
        conf=0.10,
        verbose=False
    )

    result = results[0]

    detections = []

    # Count each type of damage
    counts = {
        "corrosion": 0,
        "crack": 0,
        "dent": 0
    }

    # Process detections
    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            # Bounding box coordinates
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

            # Count damage type
            if class_name in counts:
                counts[class_name] += 1

    # Total number of defects
    total_defects = len(detections)

    # Get annotated image
    annotated_image = result.plot()

    return {
        "annotated_image": annotated_image,
        "detections": detections,
        "counts": counts,
        "total_defects": total_defects
    }