import sqlite3 as sql 

conn = sql.connect("test.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS gps_coordinates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        latitude REAL,
                        longitude REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
conn.commit()

conn.close()