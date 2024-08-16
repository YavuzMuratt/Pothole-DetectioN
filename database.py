import sqlite3
import cv2
from config import DATABASE_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS potholes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                filename TEXT,
                                date TEXT,
                                time TEXT,
                                latitude REAL,
                                longitude REAL,
                                address TEXT,
                                image BLOB
                              )''')
        self.conn.commit()

    def save_to_database(self, frame, filename, lat, lon, timestamp):
        date, time_ = timestamp.split('_')

        _, img_encoded = cv2.imencode('.jpg', frame)
        img_blob = img_encoded.tobytes()

        self.cursor.execute('''INSERT INTO potholes (filename, date, time, latitude, longitude, address, image)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (filename, date, time_, lat, lon, 'Unknown', img_blob))
        self.conn.commit()

    def close(self):
        self.conn.close()
