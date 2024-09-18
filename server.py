from flask import Flask, jsonify, request, send_file, redirect, url_for, session, flash
from flask_session import Session
import sqlite3
import io
import matplotlib.pyplot as plt
import base64
from flask import render_template

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'gizlikey55'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

DATABASE = 'pothole_detection.db'

USERNAME = 'atakumbel'
PASSWORD = 'belediye55'


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')


# Protecting routes with a login required decorator
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))

    wrap.__name__ = f.__name__
    return wrap


@app.route('/potholes', methods=['GET'])
@login_required
def get_potholes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, filename, date, time, latitude, longitude, address, status FROM potholes')  # Added status
    potholes = cursor.fetchall()
    conn.close()

    potholes_list = [dict(row) for row in potholes]
    return jsonify(potholes_list)


@app.route('/pothole/<int:pothole_id>', methods=['GET'])
@login_required
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
@login_required
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


@app.route('/pothole/<int:pothole_id>/update_status', methods=['POST'])
@login_required
def update_status(pothole_id):
    new_status = request.form['status']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE potholes SET status = ? WHERE id = ?', (new_status, pothole_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "status": new_status})


@app.route('/pothole/<int:pothole_id>/delete', methods=['POST'])
@login_required
def delete_pothole(pothole_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM potholes WHERE id = ?', (pothole_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')


@app.route('/map', methods=['GET'])
@login_required
def map_view():
    return render_template('map.html')


@app.route('/stats', methods=['GET'])
@login_required
def stats_page():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) as count FROM potholes GROUP BY status')
    data = cursor.fetchall()
    conn.close()

    statuses = [row['status'] for row in data]
    counts = [row['count'] for row in data]

    fig, ax = plt.subplots()
    ax.bar(statuses, counts, color=['red', 'orange', 'green'])
    ax.set_xlabel('Status')
    ax.set_ylabel('Number of Potholes')
    ax.set_title('Pothole Status Distribution')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)

    return render_template('stats.html', plot_url=plot_url)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
