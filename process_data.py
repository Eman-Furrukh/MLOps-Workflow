import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Use the current working directory to get the base path
BASE_DIR = os.getcwd()

# Define file paths
RAW_CSV = os.path.join(BASE_DIR, "data", "glasgow_weather_data.csv")
PROCESSED_CSV = os.path.join(BASE_DIR, "data", "preprocessed_weather_data.csv")


def preprocess_weather_data(input_path, output_path):
    """Preprocess raw weather data."""
    logging.info(f"Preprocessing data from {input_path}...")

    try:
        # Load raw data
        df = pd.read_csv(input_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Convert 'Timestamp' to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # Extract hour from timestamp
        df['Hour'] = df['Timestamp'].dt.hour

        # Create binary feature for rainy/cloudy weather
        df['Is_Rainy'] = df['Weather'].str.contains("rain|drizzle|storm|shower", case=False, na=False).astype(int)

        # Drop unused columns
        df.drop(columns=['City', 'Timestamp'], inplace=True)

        # Reorder columns for output
        cols = ['Hour', 'Temp (C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Is_Rainy']
        df = df[cols]

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save to CSV
        df.to_csv(output_path, index=False)
        logging.info("Preprocessed data saved to:")
        logging.info(output_path)
    except Exception as e:
        logging.error(f"Error preprocessing weather data: {e}")


if __name__ == "__main__":
    preprocess_weather_data(RAW_CSV, PROCESSED_CSV)
