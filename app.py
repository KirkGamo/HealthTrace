from flask import Flask, render_template, jsonify, request
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.data_utils import DataProcessor
from app.model import DiseaseOutbreakModel
from config import Config

app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static')
app.config.from_object(Config)

# Global variables to store models and data processors
models = {}
data_processors = {}

def initialize_models():
    """Initialize models for all diseases"""
    print("Initializing models...")
    
    for disease in Config.DISEASES:
        try:
            # Initialize data processor
            data_processors[disease] = DataProcessor(sequence_length=Config.SEQUENCE_LENGTH)
            
            # Load sample data to determine feature count
            data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
            if not os.path.exists(data_file):
                print(f"✗ {disease} data file not found at {data_file}")
                continue
            
            # Read data to get feature count
            df = pd.read_csv(data_file)
            # Determine feature columns (all except 'date' and including disease_cases for target)
            # The model expects all columns as input features during prediction
            feature_cols = [col for col in df.columns if col != 'date']
            # n_features is the number of input columns (which includes disease_cases as last column)
            n_features = len(feature_cols) - 1  # Subtract 1 because disease_cases is target, not input
            
            # Initialize model
            model = DiseaseOutbreakModel(
                sequence_length=Config.SEQUENCE_LENGTH,
                n_features=n_features,
                model_type='LSTM'
            )
            
            # Load trained model
            model_path = os.path.join('app', 'models', f'{disease.lower()}_forecast_model.h5')
            
            if os.path.exists(model_path):
                model.load_model(model_path)
                models[disease] = model
                print(f"✓ {disease} model loaded ({n_features} features)")
            else:
                print(f"✗ {disease} model not found at {model_path}")
                
        except Exception as e:
            print(f"Error loading {disease} model: {e}")

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html', diseases=Config.DISEASES)

@app.route('/api/forecast/<disease>')
def get_forecast(disease):
    """Get disease outbreak forecast"""
    
    if disease not in Config.DISEASES:
        return jsonify({'error': 'Disease not found'}), 404
    
    if disease not in models:
        return jsonify({'error': f'{disease} model not loaded'}), 500
    
    try:
        # Load historical data
        data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
        
        if not os.path.exists(data_file):
            return jsonify({'error': 'Historical data not found'}), 404
        
        # Process data
        data_processor = data_processors[disease]
        df = data_processor.load_data(data_file)
        scaled_data = data_processor.prepare_features(df)
        
        # Get last sequence for prediction
        last_sequence = scaled_data[-Config.SEQUENCE_LENGTH:]
        
        # Make forecast
        model = models[disease]
        predictions = model.predict_future(last_sequence, n_days=Config.FORECAST_DAYS)
        
        # Inverse transform predictions
        predicted_cases = data_processor.inverse_transform_predictions(predictions)
        
        # Prepare response
        last_date = df['date'].iloc[-1]
        forecast_dates = [
            (last_date + timedelta(days=i+1)).strftime('%Y-%m-%d')
            for i in range(Config.FORECAST_DAYS)
        ]
        
        # Get historical data for context (last 30 days)
        historical_dates = df['date'].tail(30).dt.strftime('%Y-%m-%d').tolist()
        historical_cases = df['disease_cases'].tail(30).tolist()
        
        # Calculate alert level
        avg_cases = np.mean(historical_cases)
        max_predicted = np.max(predicted_cases)
        
        if max_predicted > avg_cases * 2:
            alert_level = 'HIGH'
            alert_message = f'High outbreak risk detected! Predicted cases may reach {int(max_predicted)} cases.'
        elif max_predicted > avg_cases * 1.5:
            alert_level = 'MEDIUM'
            alert_message = f'Moderate outbreak risk. Predicted cases may reach {int(max_predicted)} cases.'
        else:
            alert_level = 'LOW'
            alert_message = f'Low outbreak risk. Cases expected to remain around {int(max_predicted)} cases.'
        
        response = {
            'disease': disease,
            'forecast_dates': forecast_dates,
            'predicted_cases': [int(max(0, x)) for x in predicted_cases],
            'historical_dates': historical_dates,
            'historical_cases': historical_cases,
            'alert_level': alert_level,
            'alert_message': alert_message,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/current_status')
def get_current_status():
    """Get current status for all diseases"""
    
    status_data = []
    
    for disease in Config.DISEASES:
        try:
            if disease not in models:
                continue
            
            # Load historical data
            data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
            
            if not os.path.exists(data_file):
                continue
            
            df = pd.read_csv(data_file, parse_dates=['date'])
            
            # Get latest data
            latest_cases = int(df['disease_cases'].iloc[-1])
            latest_date = df['date'].iloc[-1].strftime('%Y-%m-%d')
            
            # Calculate trend (last 7 days)
            recent_cases = df['disease_cases'].tail(7).values
            trend = 'increasing' if recent_cases[-1] > recent_cases[0] else 'decreasing'
            
            status_data.append({
                'disease': disease,
                'current_cases': latest_cases,
                'date': latest_date,
                'trend': trend
            })
            
        except Exception as e:
            print(f"Error getting status for {disease}: {e}")
            continue
    
    return jsonify(status_data)

@app.route('/api/climate_data/<disease>')
def get_climate_data(disease):
    """Get climate data for a disease"""
    
    if disease not in Config.DISEASES:
        return jsonify({'error': 'Disease not found'}), 404
    
    try:
        data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
        
        if not os.path.exists(data_file):
            return jsonify({'error': 'Data not found'}), 404
        
        df = pd.read_csv(data_file, parse_dates=['date'])
        
        # Get last 30 days
        df_recent = df.tail(30)
        
        response = {
            'dates': df_recent['date'].dt.strftime('%Y-%m-%d').tolist()
        }
        
        # Add available climate features (CCHAIN format)
        if 'precipitation' in df_recent.columns:
            response['precipitation'] = df_recent['precipitation'].round(2).tolist()
        if 'precipitation_7day' in df_recent.columns:
            response['precipitation_7day'] = df_recent['precipitation_7day'].round(2).tolist()
        if 'precipitation_30day' in df_recent.columns:
            response['precipitation_30day'] = df_recent['precipitation_30day'].round(2).tolist()
        if 'spi3' in df_recent.columns:
            response['spi3'] = df_recent['spi3'].round(2).tolist()
        if 'precip_anomaly' in df_recent.columns:
            response['precip_anomaly'] = df_recent['precip_anomaly'].round(2).tolist()
        
        # Legacy format support
        if 'temperature' in df_recent.columns:
            response['temperature'] = df_recent['temperature'].round(1).tolist()
        if 'humidity' in df_recent.columns:
            response['humidity'] = df_recent['humidity'].round(1).tolist()
        if 'rainfall' in df_recent.columns:
            response['rainfall'] = df_recent['rainfall'].round(1).tolist()
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feature_factors/<disease>')
def get_feature_factors(disease):
    """Get time-series feature values organized by category for charting"""
    
    if disease not in Config.DISEASES:
        return jsonify({'error': 'Disease not found'}), 404
    
    try:
        data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
        
        if not os.path.exists(data_file):
            return jsonify({'error': 'Data not found'}), 404
        
        df = pd.read_csv(data_file, parse_dates=['date'])
        
        # Get last 30 days for time-series display
        df_recent = df.tail(30)
        
        # Organize features by category with time-series data
        feature_categories = {
            'Climate & Precipitation': {
                'features': ['precipitation', 'spi3', 'spi6', 'precip_anomaly', 
                            'precipitation_7day', 'precipitation_30day'],
                'unit_map': {
                    'precipitation': 'mm', 'precipitation_7day': 'mm', 'precipitation_30day': 'mm',
                    'spi3': '', 'spi6': '', 'precip_anomaly': 'mm'
                }
            },
            'Socioeconomic': {
                'features': ['pop_count_total', 'pop_density_mean', 'avg_rad_mean'],
                'unit_map': {
                    'pop_count_total': '', 'pop_density_mean': '/km²', 'avg_rad_mean': ''
                }
            },
            'Temperature': {
                'features': ['tmin', 'tmax', 'tave', 'temp_range', 'tave_7day', 'tave_30day'],
                'unit_map': {
                    'tmin': '°C', 'tmax': '°C', 'tave': '°C', 
                    'temp_range': '°C', 'tave_7day': '°C', 'tave_30day': '°C'
                }
            },
            'Air Quality': {
                'features': ['no2', 'co', 'so2', 'o3', 'pm10', 'pm25'],
                'unit_map': {
                    'no2': 'μg/m³', 'co': 'μg/m³', 'so2': 'μg/m³', 
                    'o3': 'μg/m³', 'pm10': 'μg/m³', 'pm25': 'μg/m³'
                }
            },
            'Vegetation': {
                'features': ['ndvi'],
                'unit_map': {'ndvi': ''}
            },
            'Sanitation & Water Access': {
                'features': ['drinking_water_count', 'drinking_water_nearest',
                            'water_well_count', 'water_well_nearest',
                            'toilet_count', 'toilet_nearest',
                            'waste_basket_count', 'waste_basket_nearest',
                            'wastewater_plant_count', 'wastewater_plant_nearest'],
                'unit_map': {
                    'drinking_water_count': '', 'drinking_water_nearest': 'm',
                    'water_well_count': '', 'water_well_nearest': 'm',
                    'toilet_count': '', 'toilet_nearest': 'm',
                    'waste_basket_count': '', 'waste_basket_nearest': 'm',
                    'wastewater_plant_count': '', 'wastewater_plant_nearest': 'm'
                }
            },
            'Water Bodies': {
                'features': ['osm_wetland_nearest', 'osm_reservoir_nearest',
                            'osm_water_nearest', 'osm_riverbank_nearest',
                            'osm_river_nearest', 'osm_stream_nearest',
                            'osm_canal_nearest', 'osm_drain_nearest'],
                'unit_map': {
                    'osm_wetland_nearest': 'm', 'osm_reservoir_nearest': 'm',
                    'osm_water_nearest': 'm', 'osm_riverbank_nearest': 'm',
                    'osm_river_nearest': 'm', 'osm_stream_nearest': 'm',
                    'osm_canal_nearest': 'm', 'osm_drain_nearest': 'm'
                }
            },
            'Healthcare Access': {
                'features': ['clinic_count', 'clinic_nearest',
                            'hospital_count', 'hospital_nearest',
                            'pharmacy_count', 'pharmacy_nearest',
                            'doctors_count', 'doctors_nearest'],
                'unit_map': {
                    'clinic_count': '', 'clinic_nearest': 'm',
                    'hospital_count': '', 'hospital_nearest': 'm',
                    'pharmacy_count': '', 'pharmacy_nearest': 'm',
                    'doctors_count': '', 'doctors_nearest': 'm'
                }
            },
            'Wealth Index': {
                'features': ['rwi_mean', 'rwi_median', 'rwi_std'],
                'unit_map': {'rwi_mean': '', 'rwi_median': '', 'rwi_std': ''}
            }
        }
        
        # Populate time-series data for each category
        response = {
            'disease': disease,
            'dates': df_recent['date'].dt.strftime('%Y-%m-%d').tolist(),
            'categories': []
        }
        
        for category_name, category_data in feature_categories.items():
            category_result = {
                'name': category_name,
                'features': []
            }
            
            for feature in category_data['features']:
                if feature in df_recent.columns:
                    values = df_recent[feature].fillna(0).tolist()
                    
                    # Format feature name for display
                    display_name = feature.replace('_', ' ').title()
                    
                    # Get unit from unit_map
                    unit = category_data['unit_map'].get(feature, '')
                    
                    category_result['features'].append({
                        'name': display_name,
                        'raw_name': feature,
                        'values': values,
                        'unit': unit
                    })
            
            # Only add category if it has data
            if category_result['features']:
                response['categories'].append(category_result)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize models on startup
    initialize_models()
    
    # Run Flask app
    print("\n" + "="*60)
    print("Disease Outbreak Forecasting System")
    print("Starting Flask application...")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
