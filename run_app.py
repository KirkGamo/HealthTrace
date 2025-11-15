#!/usr/bin/env python
"""Run the HealthTrace Flask application"""

import os
import sys

# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import and run
if __name__ == '__main__':
    from flask import Flask, render_template, jsonify, request
    import numpy as np
    import pandas as pd
    from datetime import datetime, timedelta
    import json
    
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
                
                # Initialize model
                model = DiseaseOutbreakModel(
                    sequence_length=Config.SEQUENCE_LENGTH,
                    n_features=4,
                    model_type='LSTM'
                )
                
                # Load trained model
                model_path = os.path.join('app', 'models', f'{disease.lower()}_forecast_model.h5')
                
                if os.path.exists(model_path):
                    model.load_model(model_path)
                    models[disease] = model
                    print(f"✓ {disease} model loaded")
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
                'dates': df_recent['date'].dt.strftime('%Y-%m-%d').tolist(),
                'temperature': df_recent['temperature'].round(1).tolist(),
                'humidity': df_recent['humidity'].round(1).tolist(),
                'rainfall': df_recent['rainfall'].round(1).tolist()
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Initialize models on startup
    initialize_models()
    
    # Run Flask app
    print("\n" + "="*60)
    print("Disease Outbreak Forecasting System")
    print("Starting Flask application...")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
