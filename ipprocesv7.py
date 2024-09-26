import sys
import torch
import cv2
import time
import datetime
import os
from database import Database
from config import YOLO_MODEL_PATH, SAVE_DIR, CONFIDENCE_THRESHOLD


#sys.path.insert(0, os.path.abspath('D:/Programming/Pymy/Pothole Detectione/model'))


class PotholeDetector:
    def __init__(self):
        self.model = torch.load(YOLO_MODEL_PATH)
        self.model.eval()  # Ensure the model is in evaluation mode
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.database = Database()

    def detect_potholes(self, frame):
        # Convert frame to RGB as required by YOLO model
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 640))  # Resize to 640x640 as expected by YOLOv7-tiny
        img = img / 255.0  # Normalize to [0,1]
        img = torch.from_numpy(img).float().permute(2, 0, 1).unsqueeze(0)  # Convert to tensor
        with torch.no_grad():
            output = self.model(img)
        return output

    def draw_boxes_and_capture(self, frame, results, lat=None, lon=None):
        pothole_detected = False

        # Post-processing to draw bounding boxes
        for result in results:
            boxes = result.xyxy[0].cpu().numpy()  # Extract bounding boxes
            confidences = result.conf.cpu().numpy()  # Extract confidences
            classes = result.cls.cpu().numpy()  # Extract class IDs

            for i, (x1, y1, x2, y2) in enumerate(boxes):
                confidence = confidences[i]
                class_id = int(classes[i])
                label = self.model.names[class_id]

                if label == "Pothole" and confidence > CONFIDENCE_THRESHOLD:
                    pothole_detected = True
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {confidence:.2f}', (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if pothole_detected and lat is not None and lon is not None:
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            filename = f"{SAVE_DIR}/Pothole_{timestamp}_Lat_{lat}_Lon_{lon}.jpg"
            cv2.imwrite(filename, frame)

            # Save information in the database
            self.database.save_to_database(frame, filename, lat, lon, timestamp)

            time.sleep(3)

        return frame
