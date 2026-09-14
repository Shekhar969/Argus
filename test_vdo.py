import cv2
import torch
import time

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


frame_count = 0
start_time = time.time()


while True:

    success, frame = video.read()

    if not success:
        break

    results = detector.detect(
        frame,
        device=device
    )

    annotated_frame = results[0].plot()

    frame_count += 1

    elapsed_time = time.time() - start_time

    if elapsed_time > 0:
        fps = frame_count / elapsed_time
    else:
        fps = 0

    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Argus - YOLO Video Detection",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()
cv2.destroyAllWindows()

print(f"Processed frames: {frame_count}")
print(f"Average FPS: {fps:.2f}")