import cv2
from picamera2 import Picamera2
import time
from ipproces import PotholeDetector
# from ipgeolocation import IPGeolocation

def main():
    detector = PotholeDetector()
    # geolocation = IPGeolocation()

    # Initialize Picamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()

    time.sleep(2)  # Allow the camera to warm up

    while True:
        # Capture a frame
        image = picam2.capture_array()

        # Process the frame
        results = detector.detect_potholes(image)

        # Get geolocation
        lat, lon = 41.336364, 36.265604 # geolocation.get_current_location()
        if lat and lon:
            image = detector.draw_boxes_and_capture(image, results, lat, lon)

        # Display the image using OpenCV
        cv2.imshow("Pothole Detector", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    import generate_map
    generate_map.generate_map()
