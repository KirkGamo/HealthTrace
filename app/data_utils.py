import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

class DataProcessor:
    """Process historical climate and health data for disease forecasting"""
    
    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def load_data(self, filepath):
        """Load historical data from CSV file"""
        df = pd.read_csv(filepath, parse_dates=['date'])
        df = df.sort_values('date')
        return df
    
    def prepare_features(self, df):
        """Prepare features for model input - supports CCHAIN data format"""
        # Check which feature columns are available
        if 'temperature' in df.columns:
            # Original synthetic data format
            feature_columns = ['temperature', 'humidity', 'rainfall', 'disease_cases']
        else:
            # CCHAIN full feature set: climate + socioeconomic + environmental + sanitation/water + healthcare/wealth
            # Select available features, fallback if some are missing 
            available_features = []
            for col in ['precipitation', 'spi3', 'spi6', 'precip_anomaly', 
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
                       'rwi_mean', 'rwi_median', 'rwi_std']:
                if col in df.columns:
                    available_features.append(col)
            
            # Always include disease_cases as the last feature
            if 'disease_cases' in df.columns:
                available_features.append('disease_cases')
            
            feature_columns = available_features
        
        # Handle missing values
        df_clean = df[feature_columns].copy()
        df_clean = df_clean.ffill().bfill().fillna(0)
        
        features = df_clean.values
        
        # Normalize features
        scaled_features = self.scaler.fit_transform(features)
        
        return scaled_features
    
    def create_sequences(self, data):
        """Create sequences for LSTM/GRU input"""
        X, y = [], []
        
        for i in range(len(data) - self.sequence_length):
            # Input: sequence_length days of data
            X.append(data[i:i + self.sequence_length])
            # Output: disease cases for next day
            y.append(data[i + self.sequence_length, -1])  # Last column is disease_cases
        
        return np.array(X), np.array(y)
    
    def inverse_transform_predictions(self, predictions):
        """Convert normalized predictions back to original scale"""
        # Create dummy array with same shape as original features
        # Get the number of features from the scaler
        n_features = self.scaler.n_features_in_
        dummy = np.zeros((len(predictions), n_features))
        dummy[:, -1] = predictions.flatten()
        
        # Inverse transform
        inversed = self.scaler.inverse_transform(dummy)
        
        return inversed[:, -1]
    
    def generate_sample_data(self, filepath, num_days=365):
        """Generate sample historical data for demonstration"""
        np.random.seed(42)
        
        dates = pd.date_range(end=pd.Timestamp.now(), periods=num_days, freq='D')
        
        # Generate synthetic climate data (simulating Philippines climate)
        temperature = 27 + 5 * np.sin(np.linspace(0, 4*np.pi, num_days)) + np.random.normal(0, 2, num_days)
        humidity = 70 + 15 * np.sin(np.linspace(0, 4*np.pi, num_days) + np.pi/4) + np.random.normal(0, 5, num_days)
        rainfall = np.abs(150 + 100 * np.sin(np.linspace(0, 4*np.pi, num_days) + np.pi/2) + np.random.normal(0, 30, num_days))
        
        # Generate disease cases (correlated with climate factors)
        # Higher temperature and rainfall increase disease risk
        base_cases = 50
        climate_factor = (temperature - 27) * 2 + (rainfall - 150) * 0.1 + (humidity - 70) * 0.5
        disease_cases = np.maximum(0, base_cases + climate_factor + np.random.normal(0, 10, num_days))
        disease_cases = disease_cases.astype(int)
        
        df = pd.DataFrame({
            'date': dates,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'disease_cases': disease_cases
        })
        
        df.to_csv(filepath, index=False)
        print(f"Sample data generated and saved to {filepath}")
        
        return df
