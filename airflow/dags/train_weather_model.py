import pandas as pd
import os
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use the current working directory as base
BASE_DIR = os.getcwd()

# File paths
PROCESSED_CSV = os.path.join(BASE_DIR, "data", "preprocessed_weather_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "weather_model.pkl")

def train_weather_model(input_csv=PROCESSED_CSV, model_output=MODEL_PATH):
    """Train a RandomForest model to predict rainy conditions."""
    logging.info("Starting model training...")

    try:
        # Load the preprocessed dataset
        df = pd.read_csv(input_csv)

        # Split features and target
        X = df.drop(columns=["Is_Rainy"])
        y = df["Is_Rainy"]

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize and train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"[✓] Model trained successfully. Accuracy: {accuracy:.2f}")

        # Save the trained model
        os.makedirs(os.path.dirname(model_output), exist_ok=True)
        joblib.dump(model, model_output)
        logging.info(f"[✓] Trained model saved to {model_output}")
    except Exception as e:
        logging.error(f"Error during model training: {e}")

if __name__ == "__main__":
    train_weather_model()
