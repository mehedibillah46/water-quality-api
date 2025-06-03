from flask import Flask, request, jsonify, send_from_directory, send_file
import psycopg2
import json


app = Flask(__name__)
data_store = {}

@app.route('/api/data', methods=['POST'])
def receive_data():
    global data_store
    data_store = request.json
    print("Received:", data_store)
    return jsonify({"status": "ok"}), 200

@app.route('/api/data', methods=['GET'])
def send_data():
    return jsonify(data_store)

@app.route('/api/history')
def get_history():
    try:

        conn = psycopg2.connect(
    host="aws-0-eu-north-1.pooler.supabase.com",
    port=5432,
    database="postgres",
    user="postgres.weldwzaojqpsxzficwqm",
    password="LifeIsBeautiful@46",
    sslmode="require"
)

        cur = conn.cursor()
        cur.execute("""
            SELECT timestamp, dissolved_oxygen, ph, salinity, ammonium, chlorophyll
            FROM sensor_readings
            WHERE timestamp >= NOW() - INTERVAL '365 days'
            ORDER BY timestamp ASC
        """)

        rows = cur.fetchall()[::-1]  # Reverse for chronological order
        cur.close()
        conn.close()

        result = [{
            "timestamp": row[0].isoformat(),
            "dissolved_oxygen": row[1],
            "ph": row[2],
            "salinity": row[3],
            "ammonium": row[4],
            "chlorophyll": row[5]
        } for row in rows]

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
