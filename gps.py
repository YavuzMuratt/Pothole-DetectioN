import serial
from config import SERIAL_PORT, BAUD_RATE

class GPS:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        except serial.SerialException as e:
            raise Exception(f"Error opening serial port {SERIAL_PORT}: {e}")

    def get_current_location(self):
        try:
            while True:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8').strip()
                    
                    # Check if we have a valid GPRMC sentence
                    if line.startswith("$GPRMC"):
                        parts = line.split(',')
                        # GPRMC: check if we have a valid GPS fix (A = active)
                        if parts[2] == 'A':
                            lat = self._convert_to_degrees(parts[3], parts[4])
                            lon = self._convert_to_degrees(parts[5], parts[6])
                            print(f"GPS Fix Acquired: Latitude={lat}, Longitude={lon}")
                            return lat, lon

                    # Log if no valid fix is present
                    print("Waiting for GPS fix...")

        except Exception as e:
            print(f"Error getting location: {e}")
        return None, None

    def _convert_to_degrees(self, raw_value, direction):
        if not raw_value or not direction:
            return None
        
        if direction in ['N', 'S']:
            degrees = int(raw_value[:2])
            minutes = float(raw_value[2:])
        else:  # 'E' or 'W'
            degrees = int(raw_value[:3])
            minutes = float(raw_value[3:])

        decimal_degrees = degrees + (minutes / 60)

        if direction == 'S' or direction == 'W':
            decimal_degrees *= -1

        return decimal_degrees

    def close(self):
        if self.ser.is_open:
            self.ser.close()
