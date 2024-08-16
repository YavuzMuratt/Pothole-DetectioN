from flask import Flask, jsonify, request, send_file, render_template_string
import sqlite3
import io

app = Flask(__name__)
DATABASE = 'pothole_detection.db'


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/potholes', methods=['GET'])
def get_potholes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, date, time, latitude, longitude, address FROM potholes')
    potholes = cursor.fetchall()
    conn.close()

    potholes_list = [dict(row) for row in potholes]
    return jsonify(potholes_list)


@app.route('/pothole/<int:pothole_id>', methods=['GET'])
def get_pothole(pothole_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, date, time, latitude, longitude, address FROM potholes WHERE id = ?',
                   (pothole_id,))
    pothole = cursor.fetchone()
    conn.close()

    if pothole:
        return jsonify(dict(pothole))
    else:
        return jsonify({"error": "Pothole not found"}), 404


@app.route('/pothole/image/<int:pothole_id>', methods=['GET'])
def get_pothole_image(pothole_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT image FROM potholes WHERE id = ?', (pothole_id,))
    pothole = cursor.fetchone()
    conn.close()

    if pothole and pothole['image']:
        return send_file(io.BytesIO(pothole['image']), mimetype='image/jpeg')
    else:
        return jsonify({"error": "Pothole or image not found"}), 404


@app.route('/', methods=['GET'])
def home():
    # HTML template with Bootstrap and JavaScript for interactive UI
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pothole Detection Data</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {
                padding: 20px;
            }
            table {
                margin-top: 20px;
            }
            .hidden-image {
                display: none;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center">Pothole Detection Data</h1>
            <table class="table table-striped table-bordered">
                <thead class="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Filename</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Latitude</th>
                        <th>Longitude</th>
                        <th>Address</th>
                        <th>Image</th>
                    </tr>
                </thead>
                <tbody id="pothole-data">
                    <!-- Data will be inserted here by JavaScript -->
                </tbody>
            </table>
        </div>

        <script>
            // Fetch data from the /potholes API and populate the table
            fetch('/potholes')
                .then(response => response.json())
                .then(data => {
                    const tableBody = document.getElementById('pothole-data');
                    data.forEach(pothole => {
                        const row = document.createElement('tr');

                        row.innerHTML = `
                            <td>${pothole.id}</td>
                            <td>${pothole.filename}</td>
                            <td>${pothole.date}</td>
                            <td>${pothole.time}</td>
                            <td>${pothole.latitude}</td>
                            <td>${pothole.longitude}</td>
                            <td>${pothole.address}</td>
                            <td>
                                <button class="btn btn-info btn-sm" onclick="toggleImage(${pothole.id})">Show Image</button>
                                <div id="image-${pothole.id}" class="hidden-image">
                                    <img src="/pothole/image/${pothole.id}" class="img-fluid" alt="Pothole Image">
                                </div>
                            </td>
                        `;

                        tableBody.appendChild(row);
                    });
                })
                .catch(error => console.error('Error fetching pothole data:', error));

            // Function to toggle image visibility
            function toggleImage(id) {
                const imageDiv = document.getElementById(`image-${id}`);
                if (imageDiv.style.display === 'none' || imageDiv.style.display === '') {
                    imageDiv.style.display = 'block';
                } else {
                    imageDiv.style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
