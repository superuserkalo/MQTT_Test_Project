import folium
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

# Fetch all GPS data from the database
def fetch_gps_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT latitude, longitude FROM location_data")
        return cursor.fetchall()  # Returns a list of (latitude, longitude) tuples
    except mariadb.Error as e:
        print(f"Error fetching data: {e}")
        return []

# Generate the Folium map
def generate_map(gps_data):
    if gps_data:
        # Initialize a map centered around the first GPS point
        first_point = gps_data[0]
        folium_map = folium.Map(location=[first_point[0], first_point[1]], zoom_start=10)

        # Add markers for each GPS point
        for point in gps_data:
            folium.Marker([point[0], point[1]], popup=f"Lat: {point[0]}, Lon: {point[1]}").add_to(folium_map)

        # Optionally, you can connect the GPS points to visualize the path
        folium.PolyLine(gps_data, color="blue", weight=2.5, opacity=1).add_to(folium_map)

        # Save the map as an HTML file
        folium_map.save("gps_data_map.html")
        print("Map has been generated and saved as gps_data_map.html")
    else:
        print("No GPS data available to generate the map.")

# Main function to execute the visualization
if __name__ == "__main__":
    conn = connect_to_mariadb()
    if conn:
        gps_data = fetch_gps_data(conn)
        generate_map(gps_data)
        conn.close()
