import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Paths
dataset_folder = project_folder / "dataset"
models_folder = project_folder / "models"

models_folder.mkdir(exist_ok=True)

# Load training data
X_train = pd.read_csv(dataset_folder / "X_train.csv")

print("Training data loaded successfully!")

# Create Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.20,
    random_state=42
)

# Train model
model.fit(X_train)

# Save model
model_path = models_folder / "isolation_forest.pkl"
joblib.dump(model, model_path)

print("Isolation Forest model trained successfully!")
print("Model saved at:", model_path)