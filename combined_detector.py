import joblib
import pandas as pd
import sqlite3

from pathlib import Path


# =====================================
# 1. FIND PROJECT FOLDER
# =====================================

project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


# =====================================
# 2. DECISION RECOVERY FUNCTION
# =====================================

def save_decision_recovery(
    original_decision,
    corrected_decision,
    reason
):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO decision_recovery_memory
        (
            original_decision,
            corrected_decision,
            reason
        )
        VALUES (?, ?, ?)
    """, (
        original_decision,
        corrected_decision,
        reason
    ))

    connection.commit()
    connection.close()

    print("Decision Recovery Memory: Saved successfully")


# =====================================
# 3. LOAD AI MODELS
# =====================================

random_forest = joblib.load(
    project_folder / "models" / "random_forest.pkl"
)

isolation_forest = joblib.load(
    project_folder / "models" / "isolation_forest.pkl"
)

scaler = joblib.load(
    project_folder / "models" / "scaler.pkl"
)


# =====================================
# 4. GET IDENTITY DETAILS
# =====================================

print("Combined AI Brute Force Detector")
print("--------------------------------")

username = input("Enter username: ").strip().lower()
ip_address = input("Enter IP address: ").strip()
device = input("Enter device name: ").strip().lower()


# =====================================
# 5. GET LOGIN DETAILS
# =====================================

login_attempts = int(
    input("Enter total login attempts: ")
)

failed_attempts = int(
    input("Enter failed login attempts: ")
)

time_between_attempts = float(
    input("Enter average time between attempts in seconds: ")
)

unique_usernames = int(
    input("Enter number of unique usernames: ")
)

ip_reputation = float(
    input("Enter IP reputation score between 0 and 1: ")
)


# =====================================
# 6. PREPARE INPUT DATA
# =====================================

input_data = pd.DataFrame([{
    "login_attempts": login_attempts,
    "failed_attempts": failed_attempts,
    "time_between_attempts": time_between_attempts,
    "unique_usernames": unique_usernames,
    "ip_reputation": ip_reputation
}])


# =====================================
# 7. SCALE INPUT DATA
# =====================================

input_scaled = scaler.transform(input_data)


# =====================================
# 8. RANDOM FOREST PREDICTION
# =====================================

rf_prediction = random_forest.predict(input_scaled)[0]

rf_probability = random_forest.predict_proba(
    input_scaled
)[0][1]


# =====================================
# 9. ISOLATION FOREST PREDICTION
# =====================================

if_prediction = isolation_forest.predict(input_scaled)[0]

if if_prediction == -1:
    anomaly_score = 1
else:
    anomaly_score = 0


# =====================================
# 10. COMBINED RISK SCORE
# =====================================

risk_score = (
    (rf_probability * 0.7) +
    (anomaly_score * 0.3)
) * 100


# =====================================
# 11. FINAL DECISION
# =====================================

if risk_score >= 60:
    decision = "HIGH RISK"

elif risk_score >= 35:
    decision = "MEDIUM RISK"

else:
    decision = "LOW RISK"


# =====================================
# 12. CONNECT TO DATABASE
# =====================================

connection = sqlite3.connect(database_path)
cursor = connection.cursor()


# =====================================
# 13. CHECK PREVIOUS IDENTITY MEMORY
# =====================================

cursor.execute("""
    SELECT id, login_count, suspicious_count
    FROM identity_memory
    WHERE username = ?
    AND ip_address = ?
    AND device = ?
""", (
    username,
    ip_address,
    device
))

existing_identity = cursor.fetchone()


# =====================================
# 14. DECISION RECOVERY CHECK
# =====================================

if existing_identity:

    previous_suspicious_count = existing_identity[2]

    if previous_suspicious_count == 0:
        previous_decision = "LOW RISK"
    else:
        previous_decision = "SUSPICIOUS ACTIVITY"

    if previous_decision == "LOW RISK" and decision != "LOW RISK":

        save_decision_recovery(
            original_decision=previous_decision,
            corrected_decision=decision,
            reason="The same identity later showed suspicious login behavior"
        )

    elif previous_decision != "LOW RISK" and decision == "LOW RISK":

        save_decision_recovery(
            original_decision=previous_decision,
            corrected_decision=decision,
            reason="The same identity later showed normal login behavior"
        )


# =====================================
# 15. SAVE IDENTITY STABILITY MEMORY
# =====================================

if decision == "LOW RISK":
    suspicious_value = 0
else:
    suspicious_value = 1


if existing_identity:

    identity_id = existing_identity[0]
    old_login_count = existing_identity[1]
    old_suspicious_count = existing_identity[2]

    cursor.execute("""
        UPDATE identity_memory
        SET login_count = ?,
            suspicious_count = ?
        WHERE id = ?
    """, (
        old_login_count + 1,
        old_suspicious_count + suspicious_value,
        identity_id
    ))

else:

    cursor.execute("""
        INSERT INTO identity_memory
        (
            username,
            ip_address,
            device,
            login_count,
            suspicious_count
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        ip_address,
        device,
        1,
        suspicious_value
    ))


# =====================================
# 16. SAVE ATTACK PATTERN MEMORY
# =====================================

cursor.execute("""
    INSERT INTO attack_pattern_memory
    (
        ip_address,
        failed_attempts,
        login_attempts,
        time_between_attempts,
        unique_usernames,
        ip_reputation,
        risk_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    ip_address,
    failed_attempts,
    login_attempts,
    time_between_attempts,
    unique_usernames,
    ip_reputation,
    risk_score
))


# =====================================
# 17. COMMIT DATABASE CHANGES
# =====================================

connection.commit()
connection.close()


# =====================================
# 18. DISPLAY DETECTION RESULTS
# =====================================

print("\nDetection Results")
print("-----------------")

print(
    "Random Forest Prediction:",
    rf_prediction
)

print(
    "Random Forest Probability:",
    round(rf_probability * 100, 2),
    "%"
)

print(
    "Isolation Forest Anomaly:",
    anomaly_score
)

print(
    "Combined Risk Score:",
    round(risk_score, 2),
    "%"
)

print("Identity Memory: Saved successfully")
print("Attack Pattern Memory: Saved successfully")


# =====================================
# 19. DISPLAY FINAL DECISION
# =====================================

print("\nFinal Decision")
print("--------------")

if decision == "HIGH RISK":

    print("⚠️ HIGH RISK: BRUTE-FORCE ATTACK DETECTED")

elif decision == "MEDIUM RISK":

    print("⚠️ MEDIUM RISK: SUSPICIOUS LOGIN ACTIVITY")

else:

    print("✅ LOW RISK: NORMAL LOGIN ACTIVITY")