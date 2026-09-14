import cv2

from backend.app.modules.intrusion_detection.zone_selector import ZoneSelector


VIDEO_PATH = "backend/data/videos/test1.mp4"


video = cv2.VideoCapture(
    VIDEO_PATH
)

if not video.isOpened():

    raise RuntimeError(
        f"Could not open video: {VIDEO_PATH}"
    )


success, frame = video.read()

video.release()


if not success:

    raise RuntimeError(
        "Could not read the first video frame."
    )


selector = ZoneSelector(
    frame
)


points = selector.select()


print("\nSelected Zone Coordinates:")

print("[")

for point in points:

    print(
        f"    {point},"
    )

print("]")