from backend.app.modules.events.event import ArgusEvent
from backend.app.modules.intrusion_detection.evidence_manager import (
    EvidenceManager
)


class EventManager:

    def __init__(
        self,
        evidence_manager
    ):

        self.evidence_manager = evidence_manager

    def process(
        self,
        events,
        frame
    ):

        processed_events = []

        for event in events:

            if not isinstance(
                event,
                ArgusEvent
            ):
                raise TypeError(
                    "EventManager received an invalid event type."
                )

            # ------------------------------------------------
            # INTRUSION STARTED
            # ------------------------------------------------

            if event.event_type == "intrusion_started":

                evidence_path = (
                    self.evidence_manager.save_frame(
                        frame=frame,
                        camera_id=event.camera_id,
                        zone_id=event.zone_id,
                        track_id=event.track_id
                    )
                )

                event.evidence_path = evidence_path

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    " INTRUSION STARTED"
                )

                print(
                    "=" * 60
                )

                print(
                    f"Event ID    : {event.event_id}"
                )

                print(
                    f"Camera      : {event.camera_id}"
                )

                print(
                    f"Zone        : {event.zone_id}"
                )

                print(
                    f"Track ID    : {event.track_id}"
                )

                print(
                    f"Object      : {event.object_type}"
                )

                print(
                    f"Confidence  : {event.confidence:.2f}"
                )

                print(
                    f"Timestamp   : {event.timestamp.isoformat()}"
                )

                print(
                    f"Evidence    : {event.evidence_path}"
                )

                print(
                    "=" * 60
                    + "\n"
                )


            # ------------------------------------------------
            # INTRUSION ENDED
            # ------------------------------------------------

            elif event.event_type == "intrusion_ended":

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    " INTRUSION ENDED"
                )

                print(
                    "=" * 60
                )

                print(
                    f"Event ID    : {event.event_id}"
                )

                print(
                    f"Camera      : {event.camera_id}"
                )

                print(
                    f"Zone        : {event.zone_id}"
                )

                print(
                    f"Track ID    : {event.track_id}"
                )

                print(
                    f"Timestamp   : {event.timestamp.isoformat()}"
                )

                print(
                    "=" * 60
                    + "\n"
                )


            processed_events.append(
                event
            )

        return processed_events