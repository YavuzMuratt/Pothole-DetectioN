import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('pothole_detection.db')
cursor = conn.cursor()

# Create a table to store the captured images and their information
cursor.execute('''CREATE TABLE IF NOT EXISTS potholes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   filename TEXT,
                   date TEXT,
                   time TEXT,
                   latitude REAL,
                   longitude REAL,
                   address TEXT,
                   image BLOB
                  )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
