import sqlite3
import json


def generate_map():
    # Connect to SQLite database
    conn = sqlite3.connect('pothole_detection.db')
    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute('SELECT latitude, longitude, address FROM potholes')
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Prepare data for JavaScript
    locations = [{'lat': lat, 'lng': lon, 'address': address} for lat, lon, address in data]

    # HTML template for Google Maps
    html_template = '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>Pothole Locations</title>
        <script src="https://maps.googleapis.com/maps/api/js?key=ENTER_API_KEY" async defer></script>
        <script>
          function initMap() {
            if (!window.google || !window.google.maps) {
              alert('Google Maps API failed to load.');
              return;
            }

            var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 12,
              center: {lat: locations[0].lat, lng: locations[0].lng}
            });

            locations.forEach(function(location) {
              var marker = new google.maps.Marker({
                position: {lat: location.lat, lng: location.lng},
                map: map,
                title: location.address
              });

              var infowindow = new google.maps.InfoWindow({
                content: location.address
              });

              marker.addListener('click', function() {
                infowindow.open(map, marker);
              });
            });
          }

          var locations = JSON.parse('{locations}');
        </script>
      </head>
      <body onload="initMap()">
        <div id="map" style="height: 100vh; width: 100%;"></div>
      </body>
    </html>
    '''

    # Generate the HTML content
    html_content = html_template.replace('{locations}', json.dumps(locations))

    # Save the HTML content to a file
    with open('pothole_map.html', 'w') as file:
        file.write(html_content)

    print("Map has been generated and saved as 'pothole_map.html'")
