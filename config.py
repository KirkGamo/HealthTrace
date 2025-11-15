import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Model configuration
    SEQUENCE_LENGTH = 30  # Use 30 days of historical data
    FORECAST_DAYS = 14    # Forecast 14 days ahead
    
    # Model paths
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'app', 'models', 'disease_forecast_model.h5')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'app', 'data')
    
    # Diseases to track
    DISEASES = ['Dengue', 'Influenza', 'Typhoid', 'Malaria']
    
    # Features for prediction
    CLIMATE_FEATURES = ['temperature', 'humidity', 'rainfall']
    HEALTH_FEATURES = ['disease_cases']
