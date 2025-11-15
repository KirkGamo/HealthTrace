#!/usr/bin/env python
"""Simple script to test the Flask application"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from app.data_utils import DataProcessor
from app.model import DiseaseOutbreakModel
from config import Config
import json

print("Testing HealthTrace Application...")
print("="*60)

# Test 1: Data loading
print("\n1. Testing data loading...")
try:
    data_processor = DataProcessor(sequence_length=Config.SEQUENCE_LENGTH)
    data_file = os.path.join(Config.DATA_PATH, 'dengue_historical_data.csv')
    df = data_processor.load_data(data_file)
    print(f"✓ Successfully loaded {len(df)} days of historical data")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    sys.exit(1)

# Test 2: Model loading
print("\n2. Testing model loading...")
try:
    model = DiseaseOutbreakModel(
        sequence_length=Config.SEQUENCE_LENGTH,
        n_features=4,
        model_type='LSTM'
    )
    model_path = os.path.join('app', 'models', 'dengue_forecast_model.h5')
    model.load_model(model_path)
    print(f"✓ Successfully loaded Dengue forecast model")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# Test 3: Prediction
print("\n3. Testing prediction...")
try:
    scaled_data = data_processor.prepare_features(df)
    last_sequence = scaled_data[-Config.SEQUENCE_LENGTH:]
    predictions = model.predict_future(last_sequence, n_days=14)
    predicted_cases = data_processor.inverse_transform_predictions(predictions)
    
    print(f"✓ Successfully generated 14-day forecast")
    print(f"  Predicted cases range: {int(min(predicted_cases))} to {int(max(predicted_cases))}")
    print(f"  Mean predicted cases: {int(predicted_cases.mean())}")
except Exception as e:
    print(f"✗ Error making prediction: {e}")
    sys.exit(1)

# Test 4: Flask routes (simplified)
print("\n4. Testing Flask application structure...")
try:
    from app import app, models, data_processors
    
    print(f"✓ Flask app initialized successfully")
    print(f"  Loaded models for: {', '.join(models.keys())}")
    print(f"  Available routes:")
    for rule in app.url_map.iter_rules():
        if not rule.rule.startswith('/static'):
            print(f"    {rule.rule}")
except Exception as e:
    print(f"✗ Error initializing Flask: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("All tests passed! ✓")
print("="*60)
print("\nTo run the web application:")
print("  python run_app.py")
print("\nThen visit: http://localhost:5000")
