from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess
import os

# Import functions from your modules
from collect_data import fetch_weather, write_to_csv
from process_data import preprocess_weather_data
from train_weather_model import train_weather_model

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

# Define DAG
dag = DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Weather Data Collection, Processing, and Model Training Pipeline',
    schedule_interval="*/10 * * * *",  # Every 10 minutes
    catchup=False
)

RAW_CSV = os.path.join("data", "glasgow_weather_data.csv")
PROCESSED_CSV = os.path.join("data", "preprocessed_weather_data.csv")
MODEL_PATH = os.path.join("models", "weather_model.pkl")

# Task 1: Fetch and append data
def fetch_and_store_data():
    weather_data = fetch_weather()
    write_to_csv(weather_data, RAW_CSV, mode='a')  # Append mode
    subprocess.run(["dvc", "add", RAW_CSV])  # Track the raw CSV file with DVC
    subprocess.run(["dvc", "push"])  # Push the file to remote DVC storage

# Task 2: Preprocess data
def preprocess_and_store_data():
    preprocess_weather_data(RAW_CSV, PROCESSED_CSV)
    subprocess.run(["dvc", "add", PROCESSED_CSV])  # Track the preprocessed CSV file with DVC
    subprocess.run(["dvc", "push"])  # Push the preprocessed data to DVC remote storage

# Task 3: Train model
def train_weather_model_task():
    train_weather_model(PROCESSED_CSV, MODEL_PATH)
    subprocess.run(["dvc", "add", MODEL_PATH])  # Track the trained model with DVC
    subprocess.run(["dvc", "push"])  # Push the model to DVC remote storage

# Airflow tasks
fetch_data_task = PythonOperator(
    task_id='fetch_and_store_data',
    python_callable=fetch_and_store_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_and_store_data',
    python_callable=preprocess_and_store_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_weather_model_task',
    python_callable=train_weather_model_task,
    dag=dag,
)

# Set task order (Fetch -> Preprocess -> Train model)
fetch_data_task >> preprocess_data_task >> train_model_task
