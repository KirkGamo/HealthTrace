"""
Compare LSTM vs GRU model performance for disease outbreak forecasting
"""
import os
import sys
import numpy as np
import pandas as pd
import time
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_utils import DataProcessor
from config import Config

def load_and_prepare_data(disease):
    """Load and prepare data for a disease"""
    data_processor = DataProcessor(sequence_length=Config.SEQUENCE_LENGTH)
    data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
    
    df = data_processor.load_data(data_file)
    scaled_data = data_processor.prepare_features(df)
    X, y = data_processor.create_sequences(scaled_data)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    return X_train, X_val, y_train, y_val, data_processor

def evaluate_model(model_path, X_train, y_train, X_val, y_val):
    """Evaluate a model and return metrics"""
    # Load model
    model = tf.keras.models.load_model(model_path, compile=False)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Get predictions
    start_time = time.time()
    train_pred = model.predict(X_train, verbose=0)
    val_pred = model.predict(X_val, verbose=0)
    inference_time = time.time() - start_time
    
    # Calculate metrics
    train_mae = mean_absolute_error(y_train, train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    train_r2 = r2_score(y_train, train_pred)
    
    val_mae = mean_absolute_error(y_val, val_pred)
    val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
    val_r2 = r2_score(y_val, val_pred)
    
    # Model info
    total_params = model.count_params()
    
    return {
        'train_mae': train_mae,
        'train_rmse': train_rmse,
        'train_r2': train_r2,
        'val_mae': val_mae,
        'val_rmse': val_rmse,
        'val_r2': val_r2,
        'total_params': total_params,
        'inference_time': inference_time,
        'samples': len(X_train) + len(X_val)
    }

def compare_disease_models(disease):
    """Compare LSTM vs GRU for a specific disease"""
    print(f"\n{'='*80}")
    print(f"Comparing models for {disease}")
    print(f"{'='*80}\n")
    
    # Load data
    print("Loading data...")
    X_train, X_val, y_train, y_val, data_processor = load_and_prepare_data(disease)
    print(f"Train samples: {len(X_train)}, Validation samples: {len(X_val)}")
    print(f"Features: {X_train.shape[2]}, Sequence length: {X_train.shape[1]}")
    
    # Model paths
    model_dir = os.path.join('app', 'models')
    lstm_path = os.path.join(model_dir, f'{disease.lower()}_forecast_lstm.h5')
    gru_path = os.path.join(model_dir, f'{disease.lower()}_forecast_gru.h5')
    
    # Evaluate LSTM
    print("\nEvaluating LSTM model...")
    lstm_metrics = evaluate_model(lstm_path, X_train, y_train, X_val, y_val)
    
    # Evaluate GRU
    print("Evaluating GRU model...")
    gru_metrics = evaluate_model(gru_path, X_train, y_train, X_val, y_val)
    
    # Print comparison
    print(f"\n{'─'*80}")
    print(f"{'Metric':<25} {'LSTM':<20} {'GRU':<20} {'Winner':<15}")
    print(f"{'─'*80}")
    
    metrics = [
        ('Training MAE', 'train_mae', 'lower'),
        ('Training RMSE', 'train_rmse', 'lower'),
        ('Training R²', 'train_r2', 'higher'),
        ('Validation MAE', 'val_mae', 'lower'),
        ('Validation RMSE', 'val_rmse', 'lower'),
        ('Validation R²', 'val_r2', 'higher'),
        ('Total Parameters', 'total_params', 'lower'),
        ('Inference Time (s)', 'inference_time', 'lower'),
    ]
    
    for label, key, comparison in metrics:
        lstm_val = lstm_metrics[key]
        gru_val = gru_metrics[key]
        
        if comparison == 'lower':
            winner = 'LSTM' if lstm_val < gru_val else 'GRU'
            if lstm_val == gru_val:
                winner = 'TIE'
        else:  # higher is better
            winner = 'LSTM' if lstm_val > gru_val else 'GRU'
            if lstm_val == gru_val:
                winner = 'TIE'
        
        if key in ['train_mae', 'train_rmse', 'val_mae', 'val_rmse', 'train_r2', 'val_r2']:
            print(f"{label:<25} {lstm_val:<20.4f} {gru_val:<20.4f} {winner:<15}")
        elif key == 'inference_time':
            print(f"{label:<25} {lstm_val:<20.3f} {gru_val:<20.3f} {winner:<15}")
        else:
            print(f"{label:<25} {lstm_val:<20,} {gru_val:<20,} {winner:<15}")
    
    print(f"{'─'*80}\n")
    
    return {
        'disease': disease,
        'lstm': lstm_metrics,
        'gru': gru_metrics
    }

def generate_summary(results):
    """Generate overall summary of comparisons"""
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80 + "\n")
    
    # Count wins
    lstm_wins = {'train_mae': 0, 'val_mae': 0, 'val_r2': 0, 'params': 0, 'speed': 0}
    gru_wins = {'train_mae': 0, 'val_mae': 0, 'val_r2': 0, 'params': 0, 'speed': 0}
    
    for result in results:
        lstm = result['lstm']
        gru = result['gru']
        
        if lstm['train_mae'] < gru['train_mae']:
            lstm_wins['train_mae'] += 1
        else:
            gru_wins['train_mae'] += 1
            
        if lstm['val_mae'] < gru['val_mae']:
            lstm_wins['val_mae'] += 1
        else:
            gru_wins['val_mae'] += 1
            
        if lstm['val_r2'] > gru['val_r2']:
            lstm_wins['val_r2'] += 1
        else:
            gru_wins['val_r2'] += 1
            
        if lstm['total_params'] < gru['total_params']:
            lstm_wins['params'] += 1
        else:
            gru_wins['params'] += 1
            
        if lstm['inference_time'] < gru['inference_time']:
            lstm_wins['speed'] += 1
        else:
            gru_wins['speed'] += 1
    
    print("Performance Wins by Category:")
    print(f"{'─'*80}")
    print(f"{'Category':<30} {'LSTM Wins':<15} {'GRU Wins':<15}")
    print(f"{'─'*80}")
    print(f"{'Training MAE (lower better)':<30} {lstm_wins['train_mae']:<15} {gru_wins['train_mae']:<15}")
    print(f"{'Validation MAE (lower better)':<30} {lstm_wins['val_mae']:<15} {gru_wins['val_mae']:<15}")
    print(f"{'Validation R² (higher better)':<30} {lstm_wins['val_r2']:<15} {gru_wins['val_r2']:<15}")
    print(f"{'Model Parameters (fewer better)':<30} {lstm_wins['params']:<15} {gru_wins['params']:<15}")
    print(f"{'Inference Speed (faster better)':<30} {lstm_wins['speed']:<15} {gru_wins['speed']:<15}")
    print(f"{'─'*80}\n")
    
    # Average metrics
    print("Average Metrics Across All Diseases:")
    print(f"{'─'*80}")
    print(f"{'Metric':<30} {'LSTM':<25} {'GRU':<25}")
    print(f"{'─'*80}")
    
    avg_lstm_train_mae = np.mean([r['lstm']['train_mae'] for r in results])
    avg_gru_train_mae = np.mean([r['gru']['train_mae'] for r in results])
    print(f"{'Training MAE':<30} {avg_lstm_train_mae:<25.4f} {avg_gru_train_mae:<25.4f}")
    
    avg_lstm_val_mae = np.mean([r['lstm']['val_mae'] for r in results])
    avg_gru_val_mae = np.mean([r['gru']['val_mae'] for r in results])
    print(f"{'Validation MAE':<30} {avg_lstm_val_mae:<25.4f} {avg_gru_val_mae:<25.4f}")
    
    avg_lstm_val_r2 = np.mean([r['lstm']['val_r2'] for r in results])
    avg_gru_val_r2 = np.mean([r['gru']['val_r2'] for r in results])
    print(f"{'Validation R²':<30} {avg_lstm_val_r2:<25.4f} {avg_gru_val_r2:<25.4f}")
    
    avg_lstm_params = np.mean([r['lstm']['total_params'] for r in results])
    avg_gru_params = np.mean([r['gru']['total_params'] for r in results])
    print(f"{'Total Parameters':<30} {avg_lstm_params:<25,.0f} {avg_gru_params:<25,.0f}")
    
    avg_lstm_time = np.mean([r['lstm']['inference_time'] for r in results])
    avg_gru_time = np.mean([r['gru']['inference_time'] for r in results])
    print(f"{'Inference Time (s)':<30} {avg_lstm_time:<25.3f} {avg_gru_time:<25.3f}")
    print(f"{'─'*80}\n")

if __name__ == '__main__':
    diseases = Config.DISEASES
    
    print("\n" + "="*80)
    print("LSTM vs GRU MODEL COMPARISON")
    print("HealthTrace Disease Outbreak Forecasting")
    print("="*80)
    
    results = []
    for disease in diseases:
        try:
            result = compare_disease_models(disease)
            results.append(result)
        except Exception as e:
            print(f"Error comparing models for {disease}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    if results:
        generate_summary(results)
    
    print("\n" + "="*80)
    print("Comparison complete!")
    print("="*80 + "\n")
