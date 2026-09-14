import cv2
import torch
import threading
import time
import numpy as np

from backend.app.modules.detection.yolo_detector import YOLODetector
from backend.app.modules.intrusion_detection.zone import RestrictedZone
from backend.app.modules.intrusion_detection.intrusion_detector import IntrusionDetector
from backend.app.modules.intrusion_detection.evidence_manager import EvidenceManager
from backend.app.modules.intrusion_detection.zone_storage import ZoneStorage


class CameraService:

    def __init__(self):

        self.camera_id = "CAM-001"

        self.video_path = (
            "backend/data/videos/test2.mp4"
        )

        # ====================================================
        # DEVICE
        # ====================================================

        self.device = (
            "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        # ====================================================
        # YOLO
        # ====================================================

        self.detector = YOLODetector()

        # ====================================================
        # EVIDENCE
        # ====================================================

        self.evidence_manager = EvidenceManager()

        # ====================================================
        # ZONE STORAGE
        # ====================================================

        self.zone_storage = ZoneStorage(
            "backend/data/zones.json"
        )

        # ====================================================
        # RESTRICTED ZONE
        # ====================================================

        self.zone = None

        # ====================================================
        # INTRUSION DETECTOR
        # ====================================================

        self.intrusion_detector = IntrusionDetector(
            zones=[],
            camera_id=self.camera_id
        )

        # ====================================================
        # CAMERA STATE
        # ====================================================

        self.video = None

        self.latest_frame = None

        self.latest_events = []

        self.running = False

        self.thread = None

        self.lock = threading.Lock()

        # ====================================================
        # LOAD SAVED ZONE
        # ====================================================

        self._load_saved_zone()


    # ========================================================
    # LOAD SAVED ZONE
    # ========================================================

    def _load_saved_zone(self):

        saved_zone = (
            self.zone_storage.get_zone_for_camera(
                self.camera_id
            )
        )

        # ----------------------------------------------------
        # No saved zone
        # ----------------------------------------------------

        if saved_zone is None:

            print(
                f"No saved zone found for "
                f"{self.camera_id}"
            )

            return

        # ----------------------------------------------------
        # Zone information
        # ----------------------------------------------------

        zone_id = saved_zone.get(
            "zone_id"
        )

        saved_coordinates = saved_zone.get(
            "coordinates",
            []
        )

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        if len(saved_coordinates) < 3:

            print(
                f"Saved zone {zone_id} "
                f"is invalid."
            )

            return

        # ----------------------------------------------------
        # Convert JSON coordinates
        # ----------------------------------------------------

        try:

            coordinates = [
                (
                    float(point["x"]),
                    float(point["y"])
                )
                for point in saved_coordinates
            ]

        except (
            KeyError,
            TypeError,
            ValueError
        ) as error:

            print(
                f"Could not parse saved zone: "
                f"{error}"
            )

            return

        # ----------------------------------------------------
        # Load zone into runtime
        # ----------------------------------------------------

        try:

            self.set_zone(
                zone_id=zone_id,
                coordinates=coordinates
            )

            print(
                f"Loaded saved zone: "
                f"{zone_id}"
            )

            print(
                f"Loaded zone coordinates: "
                f"{coordinates}"
            )

        except Exception as error:

            print(
                f"Could not load saved zone: "
                f"{error}"
            )


    # ========================================================
    # SET / UPDATE ZONE
    # ========================================================

    def set_zone(
        self,
        zone_id,
        coordinates
    ):

        # ----------------------------------------------------
        # Validate coordinates
        # ----------------------------------------------------

        if not coordinates:

            raise ValueError(
                "Zone must contain at least one point."
            )

        if len(coordinates) < 3:

            raise ValueError(
                "Zone must contain at least three points."
            )

        # ----------------------------------------------------
        # Create RestrictedZone
        # ----------------------------------------------------

        self.zone = RestrictedZone(
            zone_id=zone_id,
            coordinates=coordinates
        )

        # ----------------------------------------------------
        # Rebuild IntrusionDetector
        # ----------------------------------------------------

        self.intrusion_detector = IntrusionDetector(
            zones=[self.zone],
            camera_id=self.camera_id
        )

        # ----------------------------------------------------
        # Debug
        # ----------------------------------------------------

        print(
            f"Zone updated: "
            f"{zone_id} "
            f"with {len(coordinates)} points"
        )

        print(
            f"Intrusion detector zones: "
            f"{[
                zone.zone_id
                for zone in self.intrusion_detector.zones
            ]}"
        )


    # ========================================================
    # SAVE ZONE
    # ========================================================

    def save_current_zone(self):

        if self.zone is None:

            raise ValueError(
                "No zone is currently configured."
            )

        coordinates = [
            (
                float(x),
                float(y)
            )
            for x, y
            in self.zone.polygon.exterior.coords[:-1]
        ]

        return self.zone_storage.save_zone(
            zone_id=self.zone.zone_id,
            camera_id=self.camera_id,
            coordinates=coordinates
        )


    # ========================================================
    # START CAMERA
    # ========================================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(
            target=self._process_camera,
            daemon=True
        )

        self.thread.start()


    # ========================================================
    # STOP CAMERA
    # ========================================================

    def stop(self):

        self.running = False

        if self.video:

            self.video.release()

            self.video = None


    # ========================================================
    # CAMERA PROCESSING
    # ========================================================

    def _process_camera(self):

        self.video = cv2.VideoCapture(
            self.video_path
        )

        # ----------------------------------------------------
        # Check video
        # ----------------------------------------------------

        if not self.video.isOpened():

            print(
                f"Could not open camera source: "
                f"{self.video_path}"
            )

            self.running = False

            return

        # ----------------------------------------------------
        # Camera information
        # ----------------------------------------------------

        print(
            f"Monitoring camera: "
            f"{self.camera_id}"
        )

        print(
            f"Using device: "
            f"{self.device}"
        )

        # ----------------------------------------------------
        # Print actual video resolution
        # ----------------------------------------------------

        width = int(
            self.video.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            self.video.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        print(
            f"Video resolution: "
            f"{width}x{height}"
        )

        # ----------------------------------------------------
        # Zone status
        # ----------------------------------------------------

        if self.zone is not None:

            print(
                f"Active restricted zone: "
                f"{self.zone.zone_id}"
            )

            print(
                "Restricted zone coordinates:"
            )

            for point in (
                self.zone.polygon
                .exterior
                .coords[:-1]
            ):

                print(
                    f"  {point}"
                )

        else:

            print(
                "No restricted zone configured."
            )

        # ====================================================
        # MAIN CAMERA LOOP
        # ====================================================

        while self.running:

            # ------------------------------------------------
            # READ FRAME
            # ------------------------------------------------

            success, frame = (
                self.video.read()
            )

            # ------------------------------------------------
            # Restart test video
            # ------------------------------------------------

            if not success:

                self.video.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    0
                )

                continue

            # ------------------------------------------------
            # YOLO TRACKING
            # ------------------------------------------------

            try:

                results = self.detector.track(
                    frame,
                    device=self.device
                )

            except Exception as error:

                print(
                    f"YOLO tracking error: "
                    f"{error}"
                )

                continue

            # ------------------------------------------------
            # YOLO result
            # ------------------------------------------------

            if not results:

                continue

            result = results[0]

            # ------------------------------------------------
            # EXTRACT TRACKED OBJECTS
            # ------------------------------------------------

            try:

                objects = (
                    self.detector.extract_tracks(
                        result
                    )
                )

            except Exception as error:

                print(
                    f"Track extraction error: "
                    f"{error}"
                )

                objects = []

            # ------------------------------------------------
            # INTRUSION DETECTION
            # ------------------------------------------------

            try:

                events = (
                    self.intrusion_detector.check(
                        objects
                    )
                )

            except Exception as error:

                print(
                    f"Intrusion detection error: "
                    f"{error}"
                )

                events = []

            # ------------------------------------------------
            # DRAW YOLO DETECTIONS
            # ------------------------------------------------

            annotated_frame = result.plot()

            # ------------------------------------------------
            # DRAW RESTRICTED ZONE
            # ------------------------------------------------

            if self.zone is not None:

                points = [
                    (
                        int(x),
                        int(y)
                    )
                    for x, y
                    in self.zone
                    .polygon
                    .exterior
                    .coords[:-1]
                ]

                if len(points) >= 3:

                    polygon = np.array(
                        points,
                        dtype=np.int32
                    )

                    # ----------------------------------------
                    # Draw polygon
                    # ----------------------------------------

                    cv2.polylines(
                        annotated_frame,
                        [polygon],
                        True,
                        (0, 0, 255),
                        3
                    )

                    # ----------------------------------------
                    # Draw zone points
                    # ----------------------------------------

                    for index, point in enumerate(
                        points
                    ):

                        cv2.circle(
                            annotated_frame,
                            point,
                            6,
                            (0, 0, 255),
                            -1
                        )

                        cv2.putText(
                            annotated_frame,
                            str(index + 1),
                            (
                                point[0] + 10,
                                point[1] - 10
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2
                        )

                    # ----------------------------------------
                    # Zone label
                    # ----------------------------------------

                    label_x = points[0][0]

                    label_y = max(
                        points[0][1] - 15,
                        25
                    )

                    cv2.putText(
                        annotated_frame,
                        self.zone.zone_id,
                        (
                            label_x,
                            label_y
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

            # ------------------------------------------------
            # STORE FRAME + EVENTS
            # ------------------------------------------------

            with self.lock:

                self.latest_frame = (
                    annotated_frame.copy()
                )

                if events:

                    self.latest_events.extend(
                        events
                    )

            # ------------------------------------------------
            # Small sleep
            # ------------------------------------------------

            time.sleep(0.001)

        # ====================================================
        # RELEASE VIDEO
        # ====================================================

        if self.video:

            self.video.release()

            self.video = None


    # ========================================================
    # GET LATEST FRAME
    # ========================================================

    def get_frame(self):

        with self.lock:

            if self.latest_frame is None:

                return None

            return self.latest_frame.copy()


    # ========================================================
    # GET EVENTS
    # ========================================================

    def get_events(self):

        with self.lock:

            events = list(
                self.latest_events
            )

            self.latest_events = []

            return events


    # ========================================================
    # CONVERT EVENT TO JSON
    # ========================================================

    def event_to_dict(
        self,
        event
    ):

        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "camera_id": event.camera_id,
            "zone_id": event.zone_id,
            "track_id": event.track_id,
            "object_type": event.object_type,
            "confidence": event.confidence,
            "evidence_path": event.evidence_path,
            "bbox": event.bbox,
        }


    # ========================================================
    # CAMERA STATUS
    # ========================================================

    def get_status(self):

        return {
            "camera_id": self.camera_id,
            "running": self.running,
            "device": self.device,
            "zone_id": (
                self.zone.zone_id
                if self.zone is not None
                else None
            )
        }


    # ========================================================
    # ZONE DEBUG
    # ========================================================

    def get_zone_debug(self):

        if self.zone is None:

            return {
                "zone_loaded": False,
                "zone_id": None,
                "coordinates": [],
                "intrusion_detector_zones": []
            }

        coordinates = [
            {
                "x": float(x),
                "y": float(y)
            }
            for x, y
            in self.zone
            .polygon
            .exterior
            .coords[:-1]
        ]

        return {
            "zone_loaded": True,
            "zone_id": self.zone.zone_id,
            "coordinates": coordinates,
            "intrusion_detector_zones": [
                zone.zone_id
                for zone
                in self.intrusion_detector.zones
            ]
        }