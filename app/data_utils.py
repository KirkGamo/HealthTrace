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
        """Prepare features for model input"""
        # Select relevant features
        feature_columns = ['temperature', 'humidity', 'rainfall', 'disease_cases']
        features = df[feature_columns].values
        
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
        dummy = np.zeros((len(predictions), 4))
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
