import cv2
import numpy as np

from runway_geometry import analyze_alignment


def analyze_runway_alignment(image, detection):
    """
    Perform runway alignment analysis using
    the runway bounding box detected by Member 1.
    """

    # Convert PIL image → OpenCV format
    image_array = np.array(image)

    image_cv = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2BGR
    )

    # Member 1 detection contains:
    # class, confidence, bbox
    bbox = detection["bbox"]

    # Send bounding box to Member 2 geometry module
    analysis = analyze_alignment(
        image_cv,
        {"bbox": bbox}
    )

    # Convert annotated OpenCV image → RGB
    annotated_image = cv2.cvtColor(
        analysis["annotated_image"],
        cv2.COLOR_BGR2RGB
    )

    analysis["annotated_image"] = annotated_image

    return analysis