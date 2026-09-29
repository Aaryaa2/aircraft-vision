from PIL import Image

from modules.damage import analyze_damage


# Load test image
image = Image.open("results/damage/test_image.png")


# Analyze image
result = analyze_damage(image)


print("\n========== DAMAGE ANALYSIS ==========")

print("Total defects:", result["total_defects"])

print("Corrosion:", result["counts"]["corrosion"])
print("Crack:", result["counts"]["crack"])
print("Dent:", result["counts"]["dent"])

print("\nDetections:")

for detection in result["detections"]:

    print(
        f"{detection['class']} "
        f"| Confidence: {detection['confidence']:.2f}"
    )