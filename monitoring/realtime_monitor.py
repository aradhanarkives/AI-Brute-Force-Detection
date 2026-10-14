import random
import time
import joblib
import pandas as pd

from pathlib import Path
from datetime import datetime

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Load trained models
random_forest = joblib.load(
    project_folder / "models" / "random_forest.pkl"
)

isolation_forest = joblib.load(
    project_folder / "models" / "isolation_forest.pkl"
)

scaler = joblib.load(
    project_folder / "models" / "scaler.pkl"
)


def detect_login(login_data):
    """
    Detect suspicious login activity.
    """

    input_data = pd.DataFrame([login_data])

    # Scale data
    input_scaled_array = scaler.transform(input_data)

    input_scaled = pd.DataFrame(
        input_scaled_array,
        columns=input_data.columns
    )

    # Random Forest prediction
    rf_prediction = random_forest.predict(input_scaled)[0]
    rf_probability = random_forest.predict_proba(input_scaled)[0][1]

    # Isolation Forest prediction
    isolation_prediction = isolation_forest.predict(input_scaled)[0]

    if isolation_prediction == -1:
        anomaly_score = 1
    else:
        anomaly_score = 0

    # Combined risk score
    risk_score = (
        (rf_probability * 0.7) +
        (anomaly_score * 0.3)
    ) * 100

    if risk_score >= 60:
        status = "HIGH RISK - BRUTE FORCE"
    elif risk_score >= 35:
        status = "MEDIUM RISK - SUSPICIOUS"
    else:
        status = "LOW RISK - NORMAL"

    return status, risk_score


print("Real-Time Brute Force Monitoring Started")
print("Press Ctrl+C to stop monitoring")
print("------------------------------------------")

try:
    while True:

        # Randomly generate login activity
        login_data = {
            "login_attempts": random.randint(1, 100),
            "failed_attempts": random.randint(0, 80),
            "time_between_attempts": random.uniform(0.1, 60),
            "unique_usernames": random.randint(1, 30),
            "ip_reputation": random.uniform(0.0, 1.0)
        }

        status, risk_score = detect_login(login_data)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nTime: {current_time}")
        print("Login Data:", login_data)
        print("Risk Score:", round(risk_score, 2), "%")
        print("Status:", status)

        if risk_score >= 60:
            print("⚠️ ALERT: Possible brute-force attack detected!")

        time.sleep(3)

except KeyboardInterrupt:
    print("\nMonitoring stopped safely.")