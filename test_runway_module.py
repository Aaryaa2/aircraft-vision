from PIL import Image
from modules.runway import analyze_runway

image = Image.open("results/runway/test_image.jpg")

result = analyze_runway(image)

print("Runway detected:", result["runway_detected"])
print("Detections:")

for detection in result["detections"]:
    print(detection)