import paho.mqtt.client as mqtt
import json
import mariadb

# Connect to MariaDB
def connect_to_mariadb():
    try:
        conn = mariadb.connect(
            user="root",  # Replace with your MariaDB username
            password="1273",  # Replace with your MariaDB password
            host="localhost",
            database="gps_data"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# Insert GPS data into the database
def insert_gps_data(conn, latitude, longitude):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO location_data (latitude, longitude) VALUES (?, ?)", (latitude, longitude))
        conn.commit()
    except mariadb.Error as e:
        print(f"Error inserting data: {e}")

# Callback when a message is received
def on_message(client, userdata, message):
    conn = userdata  # MariaDB connection passed via userdata
    gps_data = json.loads(message.payload.decode())  # Decode and load JSON data
    latitude = gps_data["latitude"]
    longitude = gps_data["longitude"]
    
    print(f"Received GPS Data: {gps_data}")
    insert_gps_data(conn, latitude, longitude)  # Insert into MariaDB

# MQTT Setup
broker_address = "localhost"
topic = "gps/data"

conn = connect_to_mariadb()
if conn:
    client = mqtt.Client(userdata=conn)  # Pass MariaDB connection via userdata
    client.on_message = on_message
    client.connect(broker_address)
    client.subscribe(topic)

    try:
        print("Listening for GPS data...")
        client.loop_forever()  # Keep the subscriber running to receive messages
    except KeyboardInterrupt:
        print("Stopping subscriber...")
    finally:
        client.disconnect()
        conn.close()
