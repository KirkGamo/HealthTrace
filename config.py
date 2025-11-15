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
    DISEASES = ['Dengue', 'Typhoid', 'Leptospirosis']
    
    # Features for prediction (CCHAIN full feature set: climate + socioeconomic + environmental + sanitation/water + healthcare/wealth)
    CLIMATE_FEATURES = ['precipitation', 'spi3', 'spi6', 'precip_anomaly', 
                       'precipitation_7day', 'precipitation_30day',
                       'pop_count_total', 'pop_density_mean', 'avg_rad_mean',
                       'tmin', 'tmax', 'tave', 'temp_range', 'tave_7day', 'tave_30day',
                       'no2', 'co', 'so2', 'o3', 'pm10', 'pm25', 'ndvi',
                       'drinking_water_count', 'drinking_water_nearest',
                       'water_well_count', 'water_well_nearest',
                       'toilet_count', 'toilet_nearest',
                       'waste_basket_count', 'waste_basket_nearest',
                       'wastewater_plant_count', 'wastewater_plant_nearest',
                       'osm_wetland_nearest', 'osm_reservoir_nearest',
                       'osm_water_nearest', 'osm_riverbank_nearest',
                       'osm_river_nearest', 'osm_stream_nearest',
                       'osm_canal_nearest', 'osm_drain_nearest',
                       'clinic_count', 'clinic_nearest',
                       'hospital_count', 'hospital_nearest',
                       'pharmacy_count', 'pharmacy_nearest',
                       'doctors_count', 'doctors_nearest',
                       'rwi_mean', 'rwi_median', 'rwi_std']
    HEALTH_FEATURES = ['disease_cases']
