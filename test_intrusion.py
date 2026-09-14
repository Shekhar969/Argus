import cv2
import torch
import numpy as np

from backend.app.modules.detection.yolo_detector import YOLODetector
from backend.app.modules.intrusion_detection.zone import RestrictedZone
from backend.app.modules.intrusion_detection.intrusion_detector import IntrusionDetector
from backend.app.modules.intrusion_detection.evidence_manager import EvidenceManager
from backend.app.modules.events.event_manager import EventManager


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO_PATH = "backend/data/videos/test1.mp4"

CAMERA_ID = "CAM-001"

ZONE_ID = "ZONE-01"


# ============================================================
# DEVICE
# ============================================================

if torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

detector = YOLODetector()

evidence_manager = EvidenceManager()

event_manager = EventManager(
    evidence_manager=evidence_manager
)


# ============================================================
# RESTRICTED ZONE
# ============================================================

zone = RestrictedZone(
    zone_id=ZONE_ID,
    coordinates=[

        (158, 488),
    (291, 463),
    (315, 518),
    (352, 513),
    (439, 657),
    (402, 672),
    (439, 772),
    (202, 825),

    ]
)


# ============================================================
# INTRUSION DETECTOR
# ============================================================

intrusion_detector = IntrusionDetector(
    zones=[zone],
    camera_id=CAMERA_ID
)


# ============================================================
# OPEN VIDEO
# ============================================================

video = cv2.VideoCapture(
    VIDEO_PATH
)

if not video.isOpened():

    raise RuntimeError(
        f"Could not open video: {VIDEO_PATH}"
    )


print(
    f"Monitoring camera: {CAMERA_ID}"
)

print(
    f"Monitoring zone: {ZONE_ID}"
)

print(
    "Press Q to quit."
)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = video.read()

    if not success:
        break


    # ========================================================
    # YOLO TRACKING
    # ========================================================

    results = detector.track(
        frame,
        device=device
    )

    result = results[0]


    # ========================================================
    # CONVERT YOLO RESULTS TO ARGUS OBJECTS
    # ========================================================

    objects = detector.extract_tracks(
        result
    )


    # ========================================================
    # INTRUSION DETECTION
    # ========================================================

    events = intrusion_detector.check(
        objects
    )


    # ========================================================
    # DRAW YOLO DETECTIONS
    # ========================================================

    annotated_frame = result.plot()


    # ========================================================
    # DRAW RESTRICTED ZONE
    # ========================================================

    zone_points = np.array(
        zone.polygon.exterior.coords[:-1],
        dtype=np.int32
    )

    cv2.polylines(
        annotated_frame,
        [zone_points],
        True,
        (0, 0, 255),
        2
    )


    # ========================================================
    # EVENT MANAGER
    # ========================================================

    event_manager.process(
        events=events,
        frame=annotated_frame
    )


    # ========================================================
    # ACTIVE INTRUSION STATUS
    # ========================================================

    active_intrusions = (
        intrusion_detector.get_active_intrusions()
    )


    if active_intrusions:

        cv2.putText(
            annotated_frame,
            "INTRUSION DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3
        )


    # ========================================================
    # CAMERA INFORMATION
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"Camera: {CAMERA_ID}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # ========================================================
    # ZONE INFORMATION
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"Zone: {ZONE_ID}",
        (30, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # ========================================================
    # ACTIVE TRACK COUNT
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"Active Intrusions: {len(active_intrusions)}",
        (30, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "Argus - Intrusion Detection",
        annotated_frame
    )


    # ========================================================
    # QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

video.release()

cv2.destroyAllWindows()

print(
    "\nArgus intrusion detection stopped."
)