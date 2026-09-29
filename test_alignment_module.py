from PIL import Image

from modules.runway import analyze_runway
from modules.alignment import analyze_runway_alignment


# Load test image
image = Image.open("results/runway/test_image.jpg")


# Member 1: detect runway
runway_result = analyze_runway(image)

print("Runway detected:", runway_result["runway_detected"])


if runway_result["runway_detected"]:

    # Take first runway detection
    detection = runway_result["detections"][0]

    # Member 2: analyze alignment
    alignment = analyze_runway_alignment(
        image,
        detection
    )

    print("\n===== ALIGNMENT RESULTS =====")

    print(
        "Lateral deviation:",
        alignment["lateral_deviation"]
    )

    print(
        "Lateral deviation (%):",
        alignment["lateral_deviation_normalized"] * 100
    )

    print(
        "Angular deviation:",
        alignment["angular_deviation"]
    )

    print(
        "Alignment status:",
        alignment["alignment_status"]
    )

    print(
        "Landing zone:",
        alignment["landing_zone"]
    )

    print(
        "Geometry source:",
        alignment["geometry_source"]
    )

else:

    print("No runway detected.")