from ultralytics import YOLO
import cv2
import time
import datetime
import os
from gps import GPS
from database import Database
from config import YOLO_MODEL_PATH, SAVE_DIR, CONFIDENCE_THRESHOLD

class PotholeDetector:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL_PATH)
        self.gps = GPS()
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.database = Database()

    def detect_potholes(self, frame):
        return self.model(frame)

    def draw_boxes_and_capture(self, frame, results):
        pothole_detected = False

        for result in results:
            for bbox in result.boxes:
                x1, y1, x2, y2 = map(int, bbox.xyxy[0].tolist())
                label = self.model.names[int(bbox.cls)]
                confidence = bbox.conf.item()

                if label == "Pothole" and confidence > CONFIDENCE_THRESHOLD:
                    pothole_detected = True
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)

        if pothole_detected:
            lat, lon = self.gps.get_current_location()
            if lat is not None and lon is not None:
                timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"{SAVE_DIR}/Pothole_{timestamp}_Lat_{lat}_Lon_{lon}.jpg"
                cv2.imwrite(filename, frame)

                # Save information in the database
                self.database.save_to_database(frame, filename, lat, lon, timestamp)

                time.sleep(3)

        return frame
