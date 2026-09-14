import cv2
import torch

from backend.app.modules.detection.yolo_detector import YOLODetector


VIDEO_PATH = "backend/data/videos/test.mp4"


if torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"


print(f"Using device: {device}")

detector = YOLODetector()

video = cv2.VideoCapture(VIDEO_PATH)

if not video.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")


while True:

    success, frame = video.read()

    if not success:
        break

    # Run YOLO tracking
    results = detector.track(
        frame,
        device=device
    )

    # Get the current frame result
    result = results[0]

    # Convert YOLO results into Argus objects
    objects = detector.extract_tracks(result)

    for obj in objects:
        print(obj)

    # Draw detections and tracking IDs
    annotated_frame = result.plot()

    # Display currently active tracking IDs
    if result.boxes.id is not None:

        track_ids = result.boxes.id.int().cpu().tolist()

        print("Active IDs:", track_ids)

    # Display video
    cv2.imshow(
        "Argus - YOLO Tracking",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()
cv2.destroyAllWindows()