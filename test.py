import pytest
import pandas as pd
import csv
import joblib
from unittest.mock import patch, MagicMock
import logging
import requests

# Import the functions to test
from collect_data import fetch_weather, write_to_csv
from process_data import preprocess_weather_data
from train_weather_model import train_weather_model


# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)


class TestDataCollection:
    """Tests for collect_data.py"""

    @patch('collect_data.requests.get')
    def test_fetch_weather_success(self, mock_get):
        """Test successful API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'main': {'temp': 15.5, 'humidity': 72},
            'weather': [{'description': 'light rain'}],
            'wind': {'speed': 3.2}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_weather()
        assert result is not None
        assert len(result) == 6
        assert isinstance(result[0], str)  # timestamp string
        assert result[2] == 15.5  # temperature
        assert result[3] == 'light rain'  # weather description

    @patch('collect_data.requests.get')
    def test_fetch_weather_failure(self, mock_get):
        """Test API failure handling."""
        mock_get.side_effect = requests.exceptions.RequestException(
            "API Error"
        )
        result = fetch_weather()
        assert result is None

    def test_write_to_csv(self, tmp_path):
        """Test CSV writing functionality."""
        test_data = [
            '2023-01-01 12:00',
            'Glasgow',
            '15.5',
            'cloudy',
            '72',
            '3.2'
        ]
        test_file = tmp_path / "weather_test.csv"

        # Test writing to new file
        write_to_csv(test_data, str(test_file))
        assert test_file.exists()

        # Verify file contents
        with open(test_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 2  # header + data row
            header = [
                'Timestamp', 'City', 'Temp (C)', 'Weather',
                'Humidity (%)', 'Wind Speed (m/s)'
            ]
            assert rows[0] == header
            assert rows[1] == test_data

        # Test appending to existing file
        new_data = [
            '2023-01-01 13:00',
            'Glasgow',
            '16.0',
            'sunny',
            '70',
            '2.8'
        ]
        write_to_csv(new_data, str(test_file))

        with open(test_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 3  # header + 2 data rows


class TestDataPreprocessing:
    """Tests for process_data.py"""

    def test_preprocessing(self, tmp_path):
        """Test the complete preprocessing pipeline."""
        # Create test raw data
        raw_data = pd.DataFrame({
            'Timestamp': [
                '2023-01-01 12:00:00',
                '2023-01-01 13:00:00',
                '2023-01-01 14:00:00'
            ],
            'City': ['Glasgow', 'Glasgow', 'Glasgow'],
            'Temp (C)': [15.5, 16.0, 17.2],
            'Weather': ['light rain', 'clear sky', 'heavy shower'],
            'Humidity (%)': [72, 70, 75],
            'Wind Speed (m/s)': [3.2, 2.8, 4.5]
        })

        # Create temp files
        input_file = tmp_path / "raw_data.csv"
        output_file = tmp_path / "processed_data.csv"

        # Save test data
        raw_data.to_csv(input_file, index=False)

        # Run preprocessing
        preprocess_weather_data(input_file, output_file)

        # Verify output
        assert output_file.exists()

        processed_data = pd.read_csv(output_file)

        # Check expected columns
        expected_cols = [
            'Hour',
            'Temp (C)',
            'Humidity (%)',
            'Wind Speed (m/s)',
            'Is_Rainy'
        ]
        assert list(processed_data.columns) == expected_cols

        # Check Hour extraction
        assert processed_data['Hour'].tolist() == [12, 13, 14]

        # Check Is_Rainy calculation
        assert processed_data['Is_Rainy'].tolist() == [1, 0, 1]

        # Check no missing values
        assert not processed_data.isnull().values.any()

    def test_preprocessing_with_missing_data(self, tmp_path):
        """Test handling of missing data."""
        # Create test data with missing values
        raw_data = pd.DataFrame({
            'Timestamp': [
                '2023-01-01 12:00:00',
                '2023-01-01 13:00:00'
            ],
            'City': ['Glasgow', None],
            'Temp (C)': [15.5, None],
            'Weather': ['light rain', None],
            'Humidity (%)': [72, None],
            'Wind Speed (m/s)': [3.2, None]
        })

        input_file = tmp_path / "raw_missing.csv"
        output_file = tmp_path / "processed_missing.csv"
        raw_data.to_csv(input_file, index=False)

        preprocess_weather_data(input_file, output_file)

        # Verify that only one row remains (the complete one)
        processed_data = pd.read_csv(output_file)
        assert len(processed_data) == 1


class TestModelTraining:
    """Tests for train_weather_model.py"""

    def test_model_training(self, tmp_path):
        """Test the model training pipeline."""
        # Create test processed data
        processed_data = pd.DataFrame({
            'Hour': list(range(12, 22)),
            'Temp (C)': [
                15.5, 16.0, 17.2, 18.1, 17.8,
                16.5, 15.2, 14.8, 14.0, 13.5
            ],
            'Humidity (%)': [72, 70, 75, 68, 72, 78, 82, 85, 88, 90],
            'Wind Speed (m/s)': [
                3.2, 2.8, 4.5, 3.7, 3.0,
                2.5, 2.0, 1.8, 1.5, 1.2
            ],
            'Is_Rainy': [1, 0, 1, 0, 0, 1, 1, 1, 0, 0]
        })

        input_file = tmp_path / "test_processed.csv"
        output_file = tmp_path / "test_model.pkl"

        # Save test data
        processed_data.to_csv(input_file, index=False)

        # Run training
        train_weather_model(
            input_csv=input_file,
            model_output=output_file
        )

        # Verify outputs
        assert output_file.exists()

        # Load the model and verify it works
        model = joblib.load(output_file)
        assert hasattr(model, 'predict')

        # Test prediction
        test_input = [[14, 16.5, 75, 3.2]]  # Hour, Temp, Humidity, Wind
        prediction = model.predict(test_input)
        assert prediction[0] in [0, 1]  # Should be either 0 or 1

    def test_model_training_empty_data(self, tmp_path):
        """Test handling of empty input data."""
        # Create empty test file
        input_file = tmp_path / "empty.csv"
        output_file = tmp_path / "empty_model.pkl"

        # Create empty DataFrame with correct columns
        pd.DataFrame(columns=[
            'Hour',
            'Temp (C)',
            'Humidity (%)',
            'Wind Speed (m/s)',
            'Is_Rainy'
        ]).to_csv(input_file, index=False)

        # Run training - should log an error
        with patch.object(logging, 'error') as mock_logging:
            train_weather_model(
                input_csv=input_file,
                model_output=output_file
            )
            mock_logging.assert_called()


if __name__ == "__main__":
    pytest.main(["-v", "test.py"])
