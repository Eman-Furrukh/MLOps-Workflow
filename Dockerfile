# Use an official Apache Airflow image as the base
FROM apache/airflow:2.7.1-python3.8

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor

# Install dependencies (including scikit-learn)
USER root
RUN pip install --no-cache-dir \
    scikit-learn==1.0.0 \
    pandas \
    joblib \
    numpy \
    scipy \
    apache-airflow-providers-sqlite \
    apache-airflow-providers-python

# Set permissions for Airflow
USER airflow

# Copy the Airflow DAGs into the container
COPY ./dags /opt/airflow/dags

# Set the working directory
WORKDIR /opt/airflow

# Define entrypoint to run the Airflow webserver and scheduler
ENTRYPOINT ["bash", "-c", "airflow db init && airflow webserver --port 8085"]
