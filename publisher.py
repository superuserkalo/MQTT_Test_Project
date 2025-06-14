import paho.mqtt.client as mqtt
import json
import random
import time

# Generate random GPS coordinates within the boundaries of Vienna
def generate_random_gps():
    # Vienna's latitudinal and longitudinal bounds
    min_lat = 48.1190
    max_lat = 48.3230
    min_lon = 16.1850
    max_lon = 16.5150

    # Generate random starting latitude and longitude within these bounds
    starting_latitude = round(random.uniform(min_lat, max_lat), 6)
    starting_longitude = round(random.uniform(min_lon, max_lon), 6)

    # Define small step size for latitude and longitude increments
    step_size_lat = 0.001  # Adjust this value as necessary for gradual change
    step_size_lon = 0.001  # Adjust this value as necessary for gradual change
    
    current_latitude = starting_latitude
    current_longitude = starting_longitude

    # Increment latitude and longitude gradually within bounds
    while True:
        lat_increment = random.uniform(-step_size_lat, step_size_lat)
        lon_increment = random.uniform(-step_size_lon, step_size_lon)

        # Update the latitude and longitude within bounds
        current_latitude = min(max_lat, max(min_lat, current_latitude + lat_increment))
        current_longitude = min(max_lon, max(min_lon, current_longitude + lon_increment))

        yield {"latitude": current_latitude, "longitude": current_longitude}

# MQTT Setup
broker_address = "localhost"
topic = "gps/data"

client = mqtt.Client()
client.connect(broker_address)

# Publish random GPS data every 5 seconds
try:
    gps_generator = generate_random_gps()
    while True:
        gps_data = next(gps_generator)
        json_data = json.dumps(gps_data)  # Convert dictionary to JSON string
        client.publish(topic, json_data)  # Publish the JSON data to the topic
        print(f"Published: {json_data}")
        time.sleep(5)  # Wait for 5 seconds before sending another GPS coordinate
except KeyboardInterrupt:
    print("Stopping publisher...")
finally:
    client.disconnect()
