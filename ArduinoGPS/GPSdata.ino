#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// Create a TinyGPS++ object
TinyGPSPlus gps;

// Set the serial port for the Neo8M GPS module
SoftwareSerial ss(21, 20); // RX, TX (adjust pins as needed)

// Variable to keep track of GPS data availability
bool gps_started = false;

void setup() {
  Serial.begin(9600);
  ss.begin(9600);

  // Wait until we receive data from the GPS module
  Serial.println("Checking if GPS module is started...");
  unsigned long start = millis();
  while (!gps_started && millis() - start < 10000) { // wait for 10 seconds
    while (ss.available() > 0) {
      gps.encode(ss.read());
      if (gps.charsProcessed() > 10) {
        gps_started = true;
        Serial.println("GPS module started successfully!");
        break;
      }
    }
  }

  if (!gps_started) {
    Serial.println("Failed to start GPS module.");
  }
}

void loop() {
  // Read data from the GPS module
  while (ss.available() > 0) {
    gps.encode(ss.read());
  }

  // If we have a valid location, send it over serial
  if (gps.location.isUpdated()) {
    Serial.print("LAT=");
    Serial.print(gps.location.lat(), 6);
    Serial.print(", LON=");
    Serial.println(gps.location.lng(), 6);
  }
}
