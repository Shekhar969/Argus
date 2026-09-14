import json
import os
import threading


class ZoneStorage:

    def __init__(self, file_path="backend/data/zones.json"):

        self.file_path = file_path

        self.lock = threading.Lock()

        self._ensure_storage()


    # ========================================================
    # ENSURE STORAGE EXISTS
    # ========================================================

    def _ensure_storage(self):

        directory = os.path.dirname(
            self.file_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )


        if not os.path.exists(
            self.file_path
        ):

            self._write_data({
                "zones": []
            })


    # ========================================================
    # READ
    # ========================================================

    def _read_data(self):

        with self.lock:

            try:

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)


                if not isinstance(
                    data,
                    dict
                ):

                    return {
                        "zones": []
                    }


                if "zones" not in data:

                    data["zones"] = []


                return data


            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):

                return {
                    "zones": []
                }


    # ========================================================
    # WRITE
    # ========================================================

    def _write_data(self, data):

        with self.lock:

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )


    # ========================================================
    # GET ALL ZONES
    # ========================================================

    def get_zones(self):

        data = self._read_data()

        return data.get(
            "zones",
            []
        )


    # ========================================================
    # GET ZONE FOR CAMERA
    # ========================================================

    def get_zone_for_camera(
        self,
        camera_id
    ):

        zones = self.get_zones()

        for zone in zones:

            if zone.get(
                "camera_id"
            ) == camera_id:

                return zone


        return None


    # ========================================================
    # SAVE / UPDATE ZONE
    # ========================================================

    def save_zone(
        self,
        zone_id,
        camera_id,
        coordinates
    ):

        with self.lock:

            try:

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):

                data = {
                    "zones": []
                }


            if "zones" not in data:

                data["zones"] = []


            zone = {
                "zone_id": zone_id,
                "camera_id": camera_id,
                "coordinates": [
                    {
                        "x": float(x),
                        "y": float(y)
                    }
                    for x, y in coordinates
                ]
            }


            # ------------------------------------------------
            # Replace existing zone for same camera
            # ------------------------------------------------

            updated = False


            for index, existing_zone in enumerate(
                data["zones"]
            ):

                if (
                    existing_zone.get(
                        "camera_id"
                    )
                    == camera_id
                ):

                    data["zones"][index] = zone

                    updated = True

                    break


            # ------------------------------------------------
            # Create new zone
            # ------------------------------------------------

            if not updated:

                data["zones"].append(
                    zone
                )


            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )


            return zone