from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

MODEL_PATH = "models/runway_best.pt"

model = YOLO(MODEL_PATH)


def analyze_runway(image):

    image_array = np.array(image.convert("RGB"))

    height, width = image_array.shape[:2]

    detections = []

    # ==================================================
    # 1. NORMAL FULL-IMAGE INFERENCE
    # ==================================================

    results = model.predict(
        source=image_array,
        conf=0.25,
        imgsz=1536,
        iou=0.7,
        augment=True,
        verbose=False
)

    result = results[0]

    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detections.append({
                "class": model.names[class_id],
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

    # ==================================================
    # 2. TILED INFERENCE
    # ==================================================

    # If the full image fails, divide it into overlapping
    # regions so small/distant runways become larger inputs.

    if not detections:

        tile_size = 768
        stride = 512

        for y in range(0, height, stride):

            for x in range(0, width, stride):

                x2 = min(x + tile_size, width)
                y2 = min(y + tile_size, height)

                tile = image_array[y:y2, x:x2]

                # Ignore extremely small edge tiles
                if tile.shape[0] < 300 or tile.shape[1] < 300:
                    continue

                tile_results = model.predict(
                    source=tile,
                    conf=0.001,
                    imgsz=1024,
                    iou=0.7,
                    augment=True,
                    verbose=False
                )

                tile_result = tile_results[0]

                if tile_result.boxes is None:
                    continue

                for box in tile_result.boxes:

                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])

                    bx1, by1, bx2, by2 = map(
                        int,
                        box.xyxy[0].tolist()
                    )

                    # Convert tile coordinates
                    # back to original image coordinates

                    bx1 += x
                    bx2 += x
                    by1 += y
                    by2 += y

                    detections.append({
                        "class": model.names[class_id],
                        "confidence": confidence,
                        "bbox": [
                            bx1,
                            by1,
                            bx2,
                            by2
                        ]
                    })

    # ==================================================
    # 3. KEEP BEST RUNWAY DETECTION
    # ==================================================

    runway_detections = [
        d for d in detections
        if d["class"] == "runway"
    ]

    if not runway_detections:

        return {
            "runway_detected": False,
            "detections": [],
            "annotated_image": image_array
        }

    # Highest-confidence runway
    best_detection = max(
        runway_detections,
        key=lambda d: d["confidence"]
    )

    # ==================================================
    # 4. DRAW RESULT
    # ==================================================

    annotated = image_array.copy()

    x1, y1, x2, y2 = best_detection["bbox"]

    cv2.rectangle(
        annotated,
        (x1, y1),
        (x2, y2),
        (0, 180, 255),
        4
    )

    label = (
        f"Runway "
        f"{best_detection['confidence'] * 100:.1f}%"
    )

    cv2.putText(
        annotated,
        label,
        (x1, max(y1 - 10, 25)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 180, 255),
        2,
        cv2.LINE_AA
    )

    return {
        "runway_detected": True,
        "detections": [best_detection],
        "annotated_image": annotated
    }