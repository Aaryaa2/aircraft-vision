from ultralytics import YOLO

# Load Member 1's runway model
model = YOLO("models/runway_best.pt")

print("Runway model loaded successfully!")
print("Classes:", model.names)

# Run prediction
results = model.predict(
    source="results/runway/test_image.jpg",
    conf=0.25,
    save=True
)

print("\nPrediction completed!")

# Print detections
for result in results:

    if result.boxes is None or len(result.boxes) == 0:
        print("No runway detected.")

    else:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            print(
                f"Detected: {class_name} | "
                f"Confidence: {confidence:.2f}"
            )

            print(
                f"Bounding Box: "
                f"[{x1}, {y1}, {x2}, {y2}]"
            )