import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# File paths
csv_path = project_folder / "dataset" / "login_data.csv"
processed_folder = project_folder / "dataset"
scaler_path = project_folder / "models" / "scaler.pkl"

# Load dataset
df = pd.read_csv(csv_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
print("\nDataset columns:")
print(df.columns)

# Separate features and target
X = df.drop("label", axis=1)
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Scale features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
scaler_path.parent.mkdir(exist_ok=True)
joblib.dump(scaler, scaler_path)

# Save processed datasets
pd.DataFrame(X_train_scaled, columns=X.columns).to_csv(
    processed_folder / "X_train.csv",
    index=False
)

pd.DataFrame(X_test_scaled, columns=X.columns).to_csv(
    processed_folder / "X_test.csv",
    index=False
)

y_train.to_csv(
    processed_folder / "y_train.csv",
    index=False
)

y_test.to_csv(
    processed_folder / "y_test.csv",
    index=False
)

print("\nPreprocessing completed successfully!")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Scaler saved at:", scaler_path)