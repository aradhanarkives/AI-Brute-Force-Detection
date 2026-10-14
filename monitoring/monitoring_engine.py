from pathlib import Path
from datetime import datetime
import sqlite3
import pandas as pd
import numpy as np
import joblib


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models"
DATABASE_PATH = PROJECT_ROOT / "project_memory.db"


FEATURES = [
    "login_attempts",
    "failed_attempts",
    "time_between_attempts",
    "unique_usernames",
    "ip_reputation"
]


# ==========================================================
# LOAD AI MODELS
# ==========================================================

def load_ai_models():
    print("Loading AI models...")

    random_forest = joblib.load(
        MODEL_PATH / "random_forest.pkl"
    )

    isolation_forest = joblib.load(
        MODEL_PATH / "isolation_forest.pkl"
    )

    scaler = joblib.load(
        MODEL_PATH / "scaler.pkl"
    )

    print("AI models loaded successfully.")

    return random_forest, isolation_forest, scaler


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS security_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            ip_address TEXT,
            login_attempts INTEGER,
            failed_attempts INTEGER,
            time_between_attempts REAL,
            unique_usernames INTEGER,
            ip_reputation REAL,
            random_forest_result INTEGER,
            isolation_forest_result INTEGER,
            final_result TEXT,
            risk_score REAL,
            decision_reason TEXT
        )
        """
    )

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


# ==========================================================
# RISK SCORE CALCULATION
# ==========================================================

def calculate_risk_score(event):
    score = 0

    if event["failed_attempts"] >= 5:
        score += 30

    if event["login_attempts"] >= 10:
        score += 25

    if event["unique_usernames"] >= 4:
        score += 20

    if event["time_between_attempts"] <= 3:
        score += 15

    if event["ip_reputation"] <= 0.30:
        score += 10

    return min(score, 100)


# ==========================================================
# SAVE SECURITY DECISION
# ==========================================================

def save_decision(decision):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO security_decisions (
            timestamp,
            username,
            ip_address,
            login_attempts,
            failed_attempts,
            time_between_attempts,
            unique_usernames,
            ip_reputation,
            random_forest_result,
            isolation_forest_result,
            final_result,
            risk_score,
            decision_reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            decision["timestamp"],
            decision.get("username", "unknown"),
            decision.get("ip_address", "unknown"),
            decision["login_attempts"],
            decision["failed_attempts"],
            decision["time_between_attempts"],
            decision["unique_usernames"],
            decision["ip_reputation"],
            decision["random_forest_result"],
            decision["isolation_forest_result"],
            decision["final_result"],
            decision["risk_score"],
            decision["decision_reason"]
        )
    )

    connection.commit()
    connection.close()

    print("Security decision saved to database.")


# ==========================================================
# ANALYZE LOGIN EVENT
# ==========================================================

def analyze_event(event):
    random_forest, isolation_forest, scaler = load_ai_models()

    input_data = pd.DataFrame(
        [
            {
                "login_attempts": event["login_attempts"],
                "failed_attempts": event["failed_attempts"],
                "time_between_attempts": event[
                    "time_between_attempts"
                ],
                "unique_usernames": event["unique_usernames"],
                "ip_reputation": event["ip_reputation"]
            }
        ]
    )

    scaled_data = scaler.transform(input_data)

    random_forest_result = int(
        random_forest.predict(scaled_data)[0]
    )

    isolation_raw_result = int(
        isolation_forest.predict(scaled_data)[0]
    )

    isolation_forest_result = (
        1 if isolation_raw_result == -1 else 0
    )

    risk_score = calculate_risk_score(event)

    if random_forest_result == 1 or isolation_forest_result == 1:
        final_result = "Attack"
        decision_reason = (
            "AI model detected suspicious login behavior"
        )

    elif risk_score >= 50:
        final_result = "Suspicious"
        decision_reason = (
            "Rule-based risk score exceeded the threshold"
        )

    else:
        final_result = "Normal"
        decision_reason = (
            "No strong attack signal detected"
        )

    decision = {
        **event,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "random_forest_result": random_forest_result,
        "isolation_forest_result": isolation_forest_result,
        "final_result": final_result,
        "risk_score": risk_score,
        "decision_reason": decision_reason
    }

    save_decision(decision)

    return decision


# ==========================================================
# TEST EVENT
# ==========================================================

if __name__ == "__main__":

    print("Starting security monitoring engine...")
    print()

    initialize_database()

    sample_event = {
        "username": "admin",
        "ip_address": "192.168.1.20",
        "login_attempts": 15,
        "failed_attempts": 14,
        "time_between_attempts": 1.2,
        "unique_usernames": 6,
        "ip_reputation": 0.15
    }

    result = analyze_event(sample_event)

    print()
    print("=" * 50)
    print("SECURITY DECISION")
    print("=" * 50)
    print("Username:", result["username"])
    print("IP Address:", result["ip_address"])
    print("Final Result:", result["final_result"])
    print("Risk Score:", result["risk_score"])
    print("Random Forest:", result["random_forest_result"])
    print("Isolation Forest:", result["isolation_forest_result"])
    print("Reason:", result["decision_reason"])
    print("=" * 50)