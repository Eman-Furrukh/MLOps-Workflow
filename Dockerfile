# Use official Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to cache dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set default command (customize this as needed)
CMD ["python", "train_weather_model.py"]
