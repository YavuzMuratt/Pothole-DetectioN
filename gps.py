import serial
from config import SERIAL_PORT, BAUD_RATE


class GPS:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        except serial.SerialException as e:
            raise Exception(f"Error opening serial port {SERIAL_PORT}: {e}")

    def get_current_location(self):
        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').strip()
                if "LAT" in line and "LON" in line:
                    parts = line.split(',')
                    lat = float(parts[0].split('=')[1])
                    lon = float(parts[1].split('=')[1])
                    return lat, lon
            return None, None
        except Exception as e:
            print(f"Error getting location: {e}")
            return 0.0, 0.0
