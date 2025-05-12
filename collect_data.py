import requests
import csv
import os
from datetime import datetime
import logging


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_KEY = "4d8970db6742d382197749ca3c923bae"
CITY = "Glasgow"
# Use the current working directory to save the file in "MLOps-Workflow\data"
OUTPUT_CSV = os.path.join(os.getcwd(), "data", "glasgow_weather_data.csv")
URL = (
    f"https://api.openweathermap.org/data/2.5/weather?q={CITY}"
    f"&appid={API_KEY}&units=metric"
)


def fetch_weather():
    """Fetch weather data from OpenWeather API."""
    logging.info("Fetching weather data...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        return {
            'Timestamp': timestamp,
            'City': CITY,
            'Temp (C)': temp,
            'Weather': weather,
            'Humidity (%)': humidity,
            'Wind Speed (m/s)': wind_speed
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None


def write_to_csv(data, path):
    """Append collected data to a CSV file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_exists = os.path.exists(path)
        
        with open(path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Timestamp', 'City', 'Temp (C)', 'Weather', 'Humidity (%)', 'Wind Speed (m/s)'])
            writer.writerow(data)

        logging.info(f"Weather data appended to {path}")
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")


if __name__ == "__main__":
    weather = fetch_weather()
    if weather:
        write_to_csv(weather, OUTPUT_CSV)
