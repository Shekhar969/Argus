from ultralytics import YOLO


class YOLODetector:

    def __init__(self, model_path="yolo11n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame, device="cpu"):
        return self.model(
            frame,
            device=device,
            verbose=False
        )

    def track(self, frame, device="cpu"):
        return self.model.track(
            frame,
            device=device,
            persist=True,
            classes=[0],
            verbose=False
        )

    def extract_tracks(self, result):
        objects = []

        if result.boxes is None:
            return objects

        boxes = result.boxes

        if boxes.id is None:
            return objects

        track_ids = boxes.id.int().cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()
        confidences = boxes.conf.cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for track_id, class_id, confidence, bbox in zip(
            track_ids,
            class_ids,
            confidences,
            coordinates
        ):
            class_name = self.model.names[class_id]

            objects.append({
                "track_id": track_id,
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bbox": bbox
            })

        return objects