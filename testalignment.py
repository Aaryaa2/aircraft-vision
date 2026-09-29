import cv2
from ultralytics import YOLO
from runway_geometry import analyze_alignment

# Load Member 1 runway model
model = YOLO("models/runway_best.pt")

# Load test image
image = cv2.imread("results/runway/test_image.jpg")

# Run runway detection
results = model.predict(
    source=image,
    conf=0.25,
    verbose=False
)

# Run Member 2 alignment analysis
analysis = analyze_alignment(
    image,
    results[0]
)

print("\n===== ALIGNMENT RESULTS =====")

print("Lateral deviation:",
      analysis["lateral_deviation"])

print("Lateral deviation (%):",
      analysis["lateral_deviation_normalized"] * 100)

print("Angular deviation:",
      analysis["angular_deviation"])

print("Alignment status:",
      analysis["alignment_status"])

print("Landing zone:",
      analysis["landing_zone"])

print("Geometry source:",
      analysis["geometry_source"])

# Save result image
cv2.imwrite(
    "results/runway/alignment_result.jpg",
    analysis["annotated_image"]
)

print("\nAnnotated result saved!")