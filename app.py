from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- Level 1: Landing Page Summary Data ---
def get_summary_data():
    conn = sqlite3.connect('climate.db')
    cursor = conn.cursor()

    cursor.execute("SELECT MIN(year), MAX(year) FROM weather")
    year_range = cursor.fetchone()

    cursor.execute("SELECT station_name, min_temp FROM weather ORDER BY min_temp ASC LIMIT 1")
    coldest_station = cursor.fetchone()

    cursor.execute("SELECT station_name, max_rainfall FROM weather ORDER BY max_rainfall DESC LIMIT 1")
    wettest_station = cursor.fetchone()

    cursor.execute("SELECT state, COUNT(*) as count FROM weather GROUP BY state ORDER BY count DESC LIMIT 1")
    most_stations_state = cursor.fetchone()

    conn.close()

    return {
        'year_range': year_range,
        'coldest_station': coldest_station,
        'wettest_station': wettest_station,
        'most_stations_state': most_stations_state
    }

@app.route('/')
def index():
    data = get_summary_data()
    return render_template("index.html", data=data)

# --- Level 2: Form and Results ---
@app.route('/weather')
def weather_form():
    return render_template('weather_view.html')

@app.route('/weather/results', methods=['POST'])
def weather_results():
    state = request.form['state']
    lat_min = float(request.form['lat_min'])
    lat_max = float(request.form['lat_max'])
    measure = request.form['measure']
    order = request.form['order']

    conn = sqlite3.connect('climate.db')
    cursor = conn.cursor()

    query = f"""
        SELECT station_name, state, region, year, min_temp, max_rainfall
        FROM weather
        WHERE state = ?
          AND year BETWEEN ? AND ?
        ORDER BY {measure} {order}
    """

    cursor.execute(query, (state, lat_min, lat_max))
    results = cursor.fetchall()
    conn.close()

    return render_template("weather_results.html", results=results, measure=measure)

if __name__ == '__main__':
    app.run(debug=True)