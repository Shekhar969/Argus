import cv2
import torch

from backend.app.modules.detection.yolo_detector import YOLODetector


IMAGE_PATH = "backend/data/images/test.webp"


if torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"


print(f"Using device: {device}")

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise RuntimeError(f"Could not load image: {IMAGE_PATH}")


detector = YOLODetector()

results = detector.detect(
    image,
    device=device
)

annotated_image = results[0].plot()

cv2.imshow(
    "Argus - YOLO Detection",
    annotated_image
)

cv2.waitKey(0)
cv2.destroyAllWindows()