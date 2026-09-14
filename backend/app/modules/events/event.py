from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class ArgusEvent:

    event_type: str

    camera_id: str

    zone_id: Optional[str] = None

    track_id: Optional[int] = None

    object_type: Optional[str] = None

    confidence: Optional[float] = None

    bbox: Optional[list] = None

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    evidence_path: Optional[str] = None

    status: str = "active"

    def to_dict(self):

        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "camera_id": self.camera_id,
            "zone_id": self.zone_id,
            "track_id": self.track_id,
            "object_type": self.object_type,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "evidence_path": self.evidence_path,
            "status": self.status
        }