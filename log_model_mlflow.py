import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn

# Paths
MODEL_PATH = os.path.join("models", "weather_model.pkl")
DATA_PATH = os.path.join("data", "preprocessed_weather_data.csv")

# MLflow config
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("weather-prediction-experiment")

# Load model and data
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)
X = df.drop(columns=["Is_Rainy"])
y = df["Is_Rainy"]
y_pred = model.predict(X)

# Evaluation metrics
acc = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average='binary', zero_division=0)
recall = recall_score(y, y_pred, average='binary', zero_division=0)
f1 = f1_score(y, y_pred, average='binary', zero_division=0)

# MLflow logging
with mlflow.start_run():
    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.sklearn.log_model(model, artifact_path="weather_rf_model")
