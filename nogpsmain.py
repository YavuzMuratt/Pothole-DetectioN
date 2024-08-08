import sqlite3
import time
import datetime
import requests
from ultralytics import YOLO
import cv2
import os

# Load yolov8 model
model = YOLO('model/modelv3.pt')

# Directory to save captured images
save_dir = 'captured_potholes'
os.makedirs(save_dir, exist_ok=True)


# Function to get current location using IP-based geolocation
def get_current_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            return lat, lon
        else:
            print("Failed to get location")
            return 0.0, 0.0  # Default coordinates
    except Exception as e:
        print(f"Error getting location: {e}")
        return 0.0, 0.0  # Default coordinates


# Function to get street and neighborhood name using Google Maps Geocoding API
def get_address_info(lat, lon):
    api_key = 'your_key'  # Replace with your API key
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    street_name = 'Unknown'
    neighborhood = 'Unknown'
    if data['status'] == 'OK':
        for result in data['results']:
            for component in result['address_components']:
                if 'route' in component['types']:
                    street_name = component['long_name']
                if 'neighborhood' in component['types']:
                    neighborhood = component['long_name']
    return street_name, neighborhood


# Function to process frame and get detections
def detect_potholes(frame):
    results = model(frame)
    return results


# Function to draw bounding boxes on the frame
def draw_boxes_and_capture(frame, results):
    pothole_detected = False
    confidence_threshold = 0.75
    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = map(int, bbox.xyxy[0].tolist())
            label = model.names[int(bbox.cls)]
            confidence = bbox.conf.item()
            print(f"Detected: {label} with confidence: {confidence}")  # Debugging statement
            if label == "Pothole" and confidence > confidence_threshold:  # Adjust according to your class label
                pothole_detected = True
                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

    if pothole_detected:
        # Capture and save the frame
        lat, lon = get_current_location()
        print(f"Coordinates: LAT={lat}, LON={lon}")  # Debugging statement
        if lat and lon:
            street_name, neighborhood = get_address_info(lat, lon)
            address = f"{street_name}, {neighborhood}"
            print(f"Address: {address}")  # Debugging statement
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            filename = f"{save_dir}/Pothole_{timestamp}_Lat_{lat}_Lon_{lon}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Pothole detected and image saved as {filename}")

            # Save the information in the database
            save_to_database(frame, filename, lat, lon, address, timestamp)

            time.sleep(3)
    return frame


# Function to save captured information into the SQLite database
def save_to_database(frame, filename, lat, lon, address, timestamp):
    conn = sqlite3.connect('pothole_detection.db')
    cursor = conn.cursor()
    date, time_ = timestamp.split('_')

    # Convert the image to binary
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_blob = img_encoded.tobytes()

    cursor.execute('''INSERT INTO potholes (filename, date, time, latitude, longitude, address, image)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (filename, date, time_, lat, lon, address, img_blob))
    conn.commit()
    conn.close()


# Open the camera feed
cap = cv2.VideoCapture(0)  # Change to video file path if necessary

if not cap.isOpened():
    print("Error: Could not open video capture")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break

    # Detect potholes
    results = detect_potholes(frame)

    # Draw bounding boxes on the frame
    frame = draw_boxes_and_capture(frame, results)

    # Display the frame
    cv2.imshow("Dedektör v2", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

import generate_map
generate_map.generate_map()
