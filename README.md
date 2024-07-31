# Pothole Detection Project

This project aims to detect potholes using a YOLOv8 model integrated with a camera feed. The project captures images of detected potholes, saves the coordinates using a GPS module, retrieves address information via Google Maps API, and stores the data in an SQLite database. Additionally, it generates a map displaying the locations of the detected potholes.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Components](#components)
  - [Main Script](#main-script)
  - [Database Setup](#database-setup)
  - [Map Generation](#map-generation)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- A webcam or a video file
- A GPS module (e.g., Neo-8M) connected via a serial port
- Google Maps API key

### Clone the Repository
```sh
git clone https://github.com/your-username/pothole-detection.git
cd pothole-detection
