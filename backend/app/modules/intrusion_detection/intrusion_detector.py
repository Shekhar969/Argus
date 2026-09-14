from backend.app.modules.events.event import ArgusEvent


class IntrusionDetector:

    def __init__(
        self,
        zones,
        camera_id,
        enter_frames=3,
        exit_frames=5
    ):

        self.zones = zones
        self.camera_id = camera_id

        self.enter_frames = enter_frames
        self.exit_frames = exit_frames

        self.inside_counts = {}
        self.outside_counts = {}

        self.active_intrusions = set()

    def check(self, objects):

        events = []

        for obj in objects:

            if obj["class_name"] != "person":
                continue

            x1, y1, x2, y2 = obj["bbox"]

            # Bottom-center of person
            foot_x = (x1 + x2) / 2
            foot_y = y2

            for zone in self.zones:

                key = (
                    zone.zone_id,
                    obj["track_id"]
                )

                inside = zone.contains(
                    foot_x,
                    foot_y
                )

                # ==================================================
                # PERSON INSIDE ZONE
                # ==================================================

                if inside:

                    self.outside_counts[key] = 0

                    self.inside_counts[key] = (
                        self.inside_counts.get(key, 0) + 1
                    )

                    # Confirm intrusion
                    if (
                        self.inside_counts[key]
                        >= self.enter_frames
                        and key not in self.active_intrusions
                    ):

                        self.active_intrusions.add(key)

                        event = ArgusEvent(
                            event_type="intrusion_started",
                            camera_id=self.camera_id,
                            zone_id=zone.zone_id,
                            track_id=obj["track_id"],
                            object_type=obj["class_name"],
                            confidence=obj["confidence"],
                            bbox=obj["bbox"]
                        )

                        events.append(event)

                # ==================================================
                # PERSON OUTSIDE ZONE
                # ==================================================

                else:

                    self.inside_counts[key] = 0

                    if key in self.active_intrusions:

                        self.outside_counts[key] = (
                            self.outside_counts.get(key, 0) + 1
                        )

                        # Confirm exit
                        if (
                            self.outside_counts[key]
                            >= self.exit_frames
                        ):

                            self.active_intrusions.remove(key)

                            event = ArgusEvent(
                                event_type="intrusion_ended",
                                camera_id=self.camera_id,
                                zone_id=zone.zone_id,
                                track_id=obj["track_id"],
                                status="ended"
                            )

                            events.append(event)

                            self.outside_counts[key] = 0

        return events

    def get_active_intrusions(self):

        return self.active_intrusions