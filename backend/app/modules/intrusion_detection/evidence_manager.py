from pathlib import Path
from datetime import datetime, timezone

import cv2


class EvidenceManager:

    def __init__(
        self,
        output_directory="backend/data/evidence/intrusions"
    ):

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_frame(
        self,
        frame,
        camera_id,
        zone_id,
        track_id
    ):

        timestamp = datetime.now(
            timezone.utc
        )

        timestamp_string = timestamp.strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = (
            f"{camera_id}_"
            f"{zone_id}_"
            f"{track_id}_"
            f"{timestamp_string}.jpg"
        )

        file_path = (
            self.output_directory /
            filename
        )

        success = cv2.imwrite(
            str(file_path),
            frame
        )

        if not success:
            raise RuntimeError(
                f"Failed to save evidence: {file_path}"
            )

        return str(file_path)