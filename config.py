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
    
    # Diseases to track (based on CCHAIN Project data for Iloilo City)
    DISEASES = ['Dengue', 'Typhoid', 'Cholera']
    
    # Features for prediction (CCHAIN enhanced data format with atmosphere features)
    CLIMATE_FEATURES = ['precipitation', 'spi3', 'spi6', 'precip_anomaly', 
                       'precipitation_7day', 'precipitation_30day',
                       'pop_count_total', 'pop_density_mean', 'avg_rad_mean',
                       'tmin', 'tmax', 'tave', 'temp_range', 'tave_7day', 'tave_30day']
    HEALTH_FEATURES = ['disease_cases']
