import requests
import time
import random
import pandas as pd
from datetime import datetime

data_log = []

while True:
    # Simulated sensor data (replace with real readings when available)
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dissolved_oxygen": round(random.uniform(6, 9), 2),
        "pH": round(random.uniform(6.5, 8), 2),
        "salinity": round(random.uniform(0.1, 0.5), 2),
        "ammonium": round(random.uniform(0.01, 0.1), 3),
        "chlorophyll": round(random.uniform(1, 15), 2)
    }

    try:
        response = requests.post("http://localhost:5000/api/data", json=data)
        print("Data sent:", data)
        data_log.append(data)

        # Save to CSV and Excel after every 5 entries
        if len(data_log) >= 5:
            df = pd.DataFrame(data_log)
            df.to_csv("sensor_data_log.csv", index=False)
            df.to_excel("sensor_data_log.xlsx", index=False)
            print("Data saved to CSV and Excel.")
            data_log = []

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
