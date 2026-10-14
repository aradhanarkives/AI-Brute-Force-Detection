import joblib
import pandas as pd
from pathlib import Path

# Find project folder
project_folder = Path(__file__).resolve().parent

# Load trained model and scaler
model_path = project_folder / "models" / "random_forest.pkl"
scaler_path = project_folder / "models" / "scaler.pkl"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

print("AI Brute Force Detection System")
print("--------------------------------")

# Get login details from user
login_attempts = int(input("Enter total login attempts: "))
failed_attempts = int(input("Enter failed login attempts: "))
time_between_attempts = float(
    input("Enter average time between attempts in seconds: ")
)
unique_usernames = int(input("Enter number of unique usernames: "))
ip_reputation = float(input("Enter IP reputation score between 0 and 1: "))

# Create input data
input_data = pd.DataFrame([{
    "login_attempts": login_attempts,
    "failed_attempts": failed_attempts,
    "time_between_attempts": time_between_attempts,
    "unique_usernames": unique_usernames,
    "ip_reputation": ip_reputation
}])10

# Scale input data
input_scaled = scaler.transform(input_data)

# Predict
prediction = model.predict(input_scaled)[0]
probability = model.predict_proba(input_scaled)[0][1]

print("\nPrediction Result")
print("-----------------")

if prediction == 1:
    print("⚠️ BRUTE-FORCE ATTACK DETECTED")
else:
    print("✅ NORMAL LOGIN ACTIVITY")

print(f"Attack probability: {probability * 100:.2f}%")