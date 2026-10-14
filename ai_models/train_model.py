import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# File paths
dataset_folder = project_folder / "dataset"
models_folder = project_folder / "models"
results_folder = project_folder / "results"

# Create folders if needed
models_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

# Load processed data
X_train = pd.read_csv(dataset_folder / "X_train.csv")
X_test = pd.read_csv(dataset_folder / "X_test.csv")

y_train = pd.read_csv(dataset_folder / "y_train.csv").squeeze()
y_test = pd.read_csv(dataset_folder / "y_test.csv").squeeze()

print("Processed dataset loaded successfully!")

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

# Train model
model.fit(X_train, y_train)

print("Random Forest model trained successfully!")

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
model_path = models_folder / "random_forest.pkl"
joblib.dump(model, model_path)

# Save results
with open(results_folder / "model_results.txt", "w") as file:
    file.write("Random Forest Brute Force Detection Results\n")
    file.write("-------------------------------------------\n")
    file.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
    file.write(classification_report(y_test, y_pred))
    file.write("\nConfusion Matrix:\n")
    file.write(str(confusion_matrix(y_test, y_pred)))

print("\nModel saved at:")
print(model_path)