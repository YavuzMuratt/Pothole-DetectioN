import cv2
from ipproces import PotholeDetector
from ipgeolocation import IPGeolocation


def main():
    detector = PotholeDetector()
    #geolocation = IPGeolocation()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        results = detector.detect_potholes(frame)

        # Get geolocation
        lat, lon = 41.336364, 36.265604 #geolocation.get_current_location()
        if lat and lon:
            frame = detector.draw_boxes_and_capture(frame, results, lat, lon)

        cv2.imshow("Pothole Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    import generate_map

    generate_map.generate_map()
