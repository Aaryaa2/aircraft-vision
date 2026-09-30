from ultralytics import YOLO
from PIL import Image
import os

MODEL_PATH = "models/runway_best.pt"

model = YOLO(MODEL_PATH)

print("\n================================")
print("RUNWAY MODEL DIRECT TEST")
print("================================")

print("Model:", MODEL_PATH)
print("Classes:", model.names)

# CHANGE THESE TWO PATHS
images = [
    
    "results/runway/new_image.jpg"
]

for image_path in images:

    print("\n--------------------------------")
    print("Testing:", image_path)
    print("--------------------------------")

    if not os.path.exists(image_path):
        print("❌ FILE NOT FOUND")
        continue

    results = model.predict(
        source=image_path,
        conf=0.001,
        imgsz=1536,
        augment=True,
        verbose=True
    )

    result = results[0]

    if result.boxes is None or len(result.boxes) == 0:
        print("❌ NO RUNWAY DETECTED")
    else:
        print("✅ DETECTIONS FOUND")

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            bbox = box.xyxy[0].tolist()

            print(
                f"Class: {model.names[class_id]} | "
                f"Confidence: {confidence:.4f} | "
                f"BBox: {bbox}"
            )

    # Save annotated image
    output_path = (
        "results/"
        + os.path.basename(image_path).split(".")[0]
        + "_direct_result.jpg"
    )

    result.save(filename=output_path)

    print("Saved:", output_path)

print("\n================================")
print("TEST COMPLETE")
print("================================")