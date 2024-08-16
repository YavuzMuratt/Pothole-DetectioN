# Pothole Detection Project

This project aims to detect potholes using a YOLOv8 model integrated with a camera feed. The project captures images of detected potholes, saves the coordinates using a GPS module, retrieves address information via Google Maps API, and stores the data in an SQLite database. Additionally, it generates a map displaying the locations of the detected potholes.

## Table of Contents
- [Usage](#usage)
- [Contributing](#contributing)
- [Prerequisites](#prequisities)

## Usage

  -- Run nogpsmain.py for ip based geolocation, it uses ipproces.py and ipgeolocation.py to run --

  Download YOLOv8 Model
  Place your YOLOv8 model file (modelv3.pt) in the model directory.


  Create SQLite Database
  Run the following script to set up the database:

  python database.py

  Running the Detection Script:
  python main.py

  You can run the server.py and display your database on the web. Can be port-forwarded via serveo or etc. to make it public

  This script will:

  - Open a camera feed.
  - Detect potholes in real-time using the YOLOv8 model.
  - Capture and save images of detected potholes along with GPS coordinates.
  - Retrieve and save address information.
  - Store all data in an SQLite database.
  - Generate a map of detected pothole locations.
  - Generating the Map
    The map is generated automatically after running the detection script. The map is saved as pothole_map.html.
  
### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- A webcam or a video file
- A GPS module (e.g., Neo-8M) connected via a serial port
- Google Maps API key


### Contributing
  Contributions are welcome! Please open an issue or submit a pull request.
