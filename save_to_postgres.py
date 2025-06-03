import requests
import time
import random
import psycopg2
from datetime import datetime
import pytz


# Connect to PostgreSQL


conn = psycopg2.connect(
    host="aws-0-eu-north-1.pooler.supabase.com",
    port=5432,
    database="postgres",
    user="postgres.weldwzaojqpsxzficwqm",
    password="LifeIsBeautiful@46",
    sslmode="require"
)

cur = conn.cursor()

while True:
    # Simulated test data (replace with real sensor data later)
    data = {
        "timestamp": datetime.now(pytz.timezone("Europe/Oslo")).isoformat(),
        "dissolved_oxygen": round(random.uniform(6, 9), 2),
        "ph": round(random.uniform(6.5, 8), 2),
        "salinity": round(random.uniform(0.1, 0.5), 2),
        "ammonium": round(random.uniform(0.01, 0.1), 3),
        "chlorophyll": round(random.uniform(1, 15), 2)
    }

    # Insert into PostgreSQL
    cur.execute("""
        INSERT INTO sensor_readings (timestamp, dissolved_oxygen, ph, salinity, ammonium, chlorophyll)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["timestamp"], data["dissolved_oxygen"], data["ph"],
        data["salinity"], data["ammonium"], data["chlorophyll"]
    ))
    conn.commit()
    print("✅ Data saved to PostgreSQL:", data)

    # Send to dashboard (optional)
    try:
        requests.post("http://localhost:5000/api/data", json=data)
    except Exception as e:
        print("Dashboard update failed:", e)

    time.sleep(10)

cur.close()
conn.close()
