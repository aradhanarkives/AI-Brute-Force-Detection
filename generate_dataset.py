import pandas as pd
import random
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).resolve().parent

# Create dataset folder if it does not exist
dataset_folder = project_folder / "dataset"
dataset_folder.mkdir(exist_ok=True)

# Dataset file path
csv_path = dataset_folder / "login_data.csv"

data = []

# Generate normal login attempts
for i in range(800):
    data.append({
        "login_attempts": random.randint(1, 5),
        "failed_attempts": random.randint(0, 2),
        "time_between_attempts": random.uniform(5, 60),
        "unique_usernames": random.randint(1, 2),
        "ip_reputation": random.uniform(0.7, 1.0),
        "label": 0
    })

# Generate brute-force login attempts
for i in range(200):
    data.append({
        "login_attempts": random.randint(20, 100),
        "failed_attempts": random.randint(10, 80),
        "time_between_attempts": random.uniform(0.1, 3),
        "unique_usernames": random.randint(5, 30),
        "ip_reputation": random.uniform(0.0, 0.4),
        "label": 1
    })

# Convert data into DataFrame
df = pd.DataFrame(data)

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save CSV file
df.to_csv(csv_path, index=False)

print("Dataset created successfully!")
print(f"Dataset location: {csv_path}")
print(f"Total rows: {len(df)}")
print(df.head())