#train_weather_model.py
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import logging


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Use the current working directory for the base path
BASE_DIR = os.getcwd()

# File paths
PROCESSED_CSV = os.path.join(BASE_DIR, "data", "preprocessed_weather_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "weather_model.pkl")


def train_weather_model(input_csv=PROCESSED_CSV, model_output=MODEL_PATH):
    """Train a weather model to predict 'Is_Rainy'."""
    logging.info("Training model...")
    try:
        # Load preprocessed data
        df = pd.read_csv(input_csv)

        # Define features and target
        X = df.drop(columns=["Is_Rainy"])
        y = df["Is_Rainy"]

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate model
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        logging.info(f"[✓] Model trained. Accuracy: {acc:.2f}")

        # Save model
        os.makedirs(os.path.dirname(model_output), exist_ok=True)
        joblib.dump(model, model_output)
        logging.info(f"[✓] Model saved to {model_output}")
    except Exception as e:
        logging.error(f"Error training the model: {e}")


if __name__ == "__main__":
    train_weather_model()
