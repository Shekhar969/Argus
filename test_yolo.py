import torch

from backend.app.modules.detection.yolo_detector import YOLODetector


if torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"


print(f"Using device: {device}")

detector = YOLODetector()

print("YOLO model loaded successfully!")