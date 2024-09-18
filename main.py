import cv2
from picamera2 import Picamera2
import time
from image_processing import PotholeDetector
from config import SAVE_DIR

def main():
    detector = PotholeDetector()

    # Initialize Picamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()

    time.sleep(2)  # Allow the camera to warm up

    while True:
        # Capture a frame from the camera
        image = picam2.capture_array()

        # Process the frame
        results = detector.detect_potholes(image)
        
        # Draw boxes and capture with GPS coordinates if a pothole is detected
        image = detector.draw_boxes_and_capture(image, results)

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
