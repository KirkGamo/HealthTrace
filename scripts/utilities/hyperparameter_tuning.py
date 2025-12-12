

"""
Hyperparameter Tuning for Disease Outbreak Forecasting Models

This script performs comprehensive hyperparameter tuning for LSTM/GRU models,
testing different optimizers and their configurations. All results are recorded
for analysis and comparison.

Current Optimizer: Adam
Tuning Parameters:
- Learning rates
- Optimizer types (Adam, RMSprop, SGD)
- Batch sizes
- LSTM/GRU units
- Dropout rates
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.optimizers import Adam, RMSprop, SGD
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_utils import DataProcessor
from config import Config


class HyperparameterTuner:
    """Hyperparameter tuning for disease outbreak models"""
    
    def __init__(self, disease='Dengue', model_type='LSTM'):
        self.disease = disease
        self.model_type = model_type
        self.results = []
        self.results_dir = 'hyperparameter_results'
        os.makedirs(self.results_dir, exist_ok=True)
        
    def load_data(self):
        """Load and prepare data for training"""
        print(f"\nLoading data for {self.disease}...")
        
        data_processor = DataProcessor(sequence_length=Config.SEQUENCE_LENGTH)
        data_file = os.path.join(Config.DATA_PATH, f'{self.disease.lower()}_historical_data.csv')
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        df = data_processor.load_data(data_file)
        scaled_data = data_processor.prepare_features(df)
        X, y = data_processor.create_sequences(scaled_data)
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, shuffle=False
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, shuffle=False
        )
        
        print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def build_model(self, config):
        """Build model with specified configuration"""
        model = Sequential()
        
        sequence_length = config['sequence_length']
        n_features = config['n_features']
        units = config['units']
        dropout = config['dropout']
        
        if self.model_type == 'LSTM':
            model.add(LSTM(units=units, return_sequences=True,
                          input_shape=(sequence_length, n_features)))
            model.add(Dropout(dropout))
            model.add(LSTM(units=units//2, return_sequences=False))
            model.add(Dropout(dropout))
        else:  # GRU
            model.add(GRU(units=units, return_sequences=True,
                         input_shape=(sequence_length, n_features)))
            model.add(Dropout(dropout))
            model.add(GRU(units=units//2, return_sequences=False))
            model.add(Dropout(dropout))
        
        model.add(Dense(units=32, activation='relu'))
        model.add(Dropout(dropout))
        model.add(Dense(units=1))
        
        # Get optimizer based on configuration
        optimizer = self.get_optimizer(config)
        
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae', 'mse'])
        
        return model
    
    def get_optimizer(self, config):
        """Get optimizer instance based on configuration"""
        opt_name = config['optimizer']
        lr = config['learning_rate']
        
        if opt_name == 'Adam':
            return Adam(learning_rate=lr, beta_1=config.get('beta_1', 0.9), 
                       beta_2=config.get('beta_2', 0.999))
        elif opt_name == 'RMSprop':
            return RMSprop(learning_rate=lr, rho=config.get('rho', 0.9))
        elif opt_name == 'SGD':
            return SGD(learning_rate=lr, momentum=config.get('momentum', 0.0), 
                      nesterov=config.get('nesterov', False))
        else:
            return Adam(learning_rate=lr)
    
    def train_and_evaluate(self, config, X_train, X_val, X_test, y_train, y_val, y_test):
        """Train model with given configuration and evaluate"""
        
        print(f"\n{'='*70}")
        print(f"Training Configuration #{len(self.results) + 1}")
        print(f"{'='*70}")
        print(f"Model Type: {self.model_type}")
        print(f"Optimizer: {config['optimizer']}")
        print(f"Learning Rate: {config['learning_rate']}")
        print(f"Batch Size: {config['batch_size']}")
        print(f"Units: {config['units']}")
        print(f"Dropout: {config['dropout']}")
        if config['optimizer'] == 'Adam':
            print(f"Beta_1: {config.get('beta_1', 0.9)}, Beta_2: {config.get('beta_2', 0.999)}")
        elif config['optimizer'] == 'RMSprop':
            print(f"Rho: {config.get('rho', 0.9)}")
        elif config['optimizer'] == 'SGD':
            print(f"Momentum: {config.get('momentum', 0.0)}, Nesterov: {config.get('nesterov', False)}")
        print(f"{'='*70}\n")
        
        # Build model
        model = self.build_model(config)
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        )
        
        # Train
        start_time = datetime.now()
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=config['epochs'],
            batch_size=config['batch_size'],
            callbacks=[early_stop],
            verbose=1
        )
        training_time = (datetime.now() - start_time).total_seconds()
        
        # Evaluate on training set
        train_metrics = model.evaluate(X_train, y_train, verbose=0)
        train_loss, train_mae, train_mse = train_metrics
        
        # Evaluate on validation set
        val_metrics = model.evaluate(X_val, y_val, verbose=0)
        val_loss, val_mae, val_mse = val_metrics
        
        # Evaluate on test set
        test_metrics = model.evaluate(X_test, y_test, verbose=0)
        test_loss, test_mae, test_mse = test_metrics
        
        # Get predictions for additional metrics
        y_train_pred = model.predict(X_train, verbose=0)
        y_val_pred = model.predict(X_val, verbose=0)
        y_test_pred = model.predict(X_test, verbose=0)
        
        # Calculate R² scores
        train_r2 = 1 - (np.sum((y_train - y_train_pred.flatten())**2) / 
                       np.sum((y_train - np.mean(y_train))**2))
        val_r2 = 1 - (np.sum((y_val - y_val_pred.flatten())**2) / 
                     np.sum((y_val - np.mean(y_val))**2))
        test_r2 = 1 - (np.sum((y_test - y_test_pred.flatten())**2) / 
                      np.sum((y_test - np.mean(y_test))**2))
        
        # Calculate RMSE
        train_rmse = np.sqrt(train_mse)
        val_rmse = np.sqrt(val_mse)
        test_rmse = np.sqrt(test_mse)
        
        # Store results
        result = {
            'config_id': len(self.results) + 1,
            'timestamp': datetime.now().isoformat(),
            'disease': self.disease,
            'model_type': self.model_type,
            
            # Configuration
            'configuration': {
                'optimizer': config['optimizer'],
                'learning_rate': config['learning_rate'],
                'batch_size': config['batch_size'],
                'units': config['units'],
                'dropout': config['dropout'],
                'epochs': config['epochs'],
                'sequence_length': config['sequence_length'],
            },
            
            # Optimizer-specific parameters
            'optimizer_params': {},
            
            # Training Results
            'training_results': {
                'loss': float(train_loss),
                'mae': float(train_mae),
                'mse': float(train_mse),
                'rmse': float(train_rmse),
                'r2_score': float(train_r2),
                'epochs_trained': len(history.history['loss']),
                'training_time_seconds': training_time,
            },
            
            # Validation Results
            'validation_results': {
                'loss': float(val_loss),
                'mae': float(val_mae),
                'mse': float(val_mse),
                'rmse': float(val_rmse),
                'r2_score': float(val_r2),
            },
            
            # Test Results
            'test_results': {
                'loss': float(test_loss),
                'mae': float(test_mae),
                'mse': float(test_mse),
                'rmse': float(test_rmse),
                'r2_score': float(test_r2),
            },
            
            # Training History
            'history': {
                'train_loss': [float(x) for x in history.history['loss']],
                'val_loss': [float(x) for x in history.history['val_loss']],
                'train_mae': [float(x) for x in history.history['mae']],
                'val_mae': [float(x) for x in history.history['val_mae']],
            }
        }
        
        # Add optimizer-specific parameters
        if config['optimizer'] == 'Adam':
            result['optimizer_params'] = {
                'beta_1': config.get('beta_1', 0.9),
                'beta_2': config.get('beta_2', 0.999),
            }
        elif config['optimizer'] == 'RMSprop':
            result['optimizer_params'] = {
                'rho': config.get('rho', 0.9),
            }
        elif config['optimizer'] == 'SGD':
            result['optimizer_params'] = {
                'momentum': config.get('momentum', 0.0),
                'nesterov': config.get('nesterov', False),
            }
        
        self.results.append(result)
        
        # Print results
        print(f"\n{'='*70}")
        print("TRAINING RESULTS:")
        print(f"  Loss: {train_loss:.6f} | MAE: {train_mae:.6f} | RMSE: {train_rmse:.6f} | R²: {train_r2:.6f}")
        print("\nVALIDATION RESULTS:")
        print(f"  Loss: {val_loss:.6f} | MAE: {val_mae:.6f} | RMSE: {val_rmse:.6f} | R²: {val_r2:.6f}")
        print("\nTEST RESULTS:")
        print(f"  Loss: {test_loss:.6f} | MAE: {test_mae:.6f} | RMSE: {test_rmse:.6f} | R²: {test_r2:.6f}")
        print(f"\nEpochs Trained: {len(history.history['loss'])}")
        print(f"Training Time: {training_time:.2f} seconds")
        print(f"{'='*70}\n")
        
        return result
    
    def run_tuning(self, configurations):
        """Run hyperparameter tuning with multiple configurations"""
        
        # Load data once
        X_train, X_val, X_test, y_train, y_val, y_test = self.load_data()
        
        # Add data shape info to configs
        for config in configurations:
            config['sequence_length'] = X_train.shape[1]
            config['n_features'] = X_train.shape[2]
        
        # Train and evaluate each configuration
        for i, config in enumerate(configurations):
            print(f"\n\n{'#'*70}")
            print(f"# Configuration {i+1}/{len(configurations)}")
            print(f"{'#'*70}")
            
            try:
                self.train_and_evaluate(config, X_train, X_val, X_test, 
                                       y_train, y_val, y_test)
            except Exception as e:
                print(f"Error with configuration {i+1}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Save all results
        self.save_results()
        
        # Print summary
        self.print_summary()
    
    def save_results(self):
        """Save results to JSON and CSV files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save detailed JSON
        json_file = os.path.join(
            self.results_dir, 
            f'{self.disease}_{self.model_type}_tuning_{timestamp}.json'
        )
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Detailed results saved to: {json_file}")
        
        # Create summary CSV
        summary_data = []
        for r in self.results:
            row = {
                'Config_ID': r['config_id'],
                'Disease': r['disease'],
                'Model_Type': r['model_type'],
                'Optimizer': r['configuration']['optimizer'],
                'Learning_Rate': r['configuration']['learning_rate'],
                'Batch_Size': r['configuration']['batch_size'],
                'Units': r['configuration']['units'],
                'Dropout': r['configuration']['dropout'],
                
                # Training metrics
                'Train_Loss': r['training_results']['loss'],
                'Train_MAE': r['training_results']['mae'],
                'Train_RMSE': r['training_results']['rmse'],
                'Train_R2': r['training_results']['r2_score'],
                
                # Validation metrics
                'Val_Loss': r['validation_results']['loss'],
                'Val_MAE': r['validation_results']['mae'],
                'Val_RMSE': r['validation_results']['rmse'],
                'Val_R2': r['validation_results']['r2_score'],
                
                # Test metrics
                'Test_Loss': r['test_results']['loss'],
                'Test_MAE': r['test_results']['mae'],
                'Test_RMSE': r['test_results']['rmse'],
                'Test_R2': r['test_results']['r2_score'],
                
                'Epochs_Trained': r['training_results']['epochs_trained'],
                'Training_Time_Sec': r['training_results']['training_time_seconds'],
            }
            
            # Add optimizer-specific params
            for key, val in r['optimizer_params'].items():
                row[f'Opt_{key}'] = val
            
            summary_data.append(row)
        
        df = pd.DataFrame(summary_data)
        csv_file = os.path.join(
            self.results_dir, 
            f'{self.disease}_{self.model_type}_summary_{timestamp}.csv'
        )
        df.to_csv(csv_file, index=False)
        print(f"✓ Summary CSV saved to: {csv_file}")
    
    def print_summary(self):
        """Print summary of all configurations"""
        print(f"\n\n{'='*80}")
        print(f"HYPERPARAMETER TUNING SUMMARY - {self.disease} {self.model_type}")
        print(f"{'='*80}\n")
        
        if not self.results:
            print("No results to display.")
            return
        
        # Find best configuration by test MAE
        best_result = min(self.results, key=lambda x: x['test_results']['mae'])
        
        print(f"Total Configurations Tested: {len(self.results)}\n")
        
        print("BEST CONFIGURATION (by Test MAE):")
        print(f"  Config ID: {best_result['config_id']}")
        print(f"  Optimizer: {best_result['configuration']['optimizer']}")
        print(f"  Learning Rate: {best_result['configuration']['learning_rate']}")
        print(f"  Batch Size: {best_result['configuration']['batch_size']}")
        print(f"  Units: {best_result['configuration']['units']}")
        print(f"  Dropout: {best_result['configuration']['dropout']}")
        
        if best_result['optimizer_params']:
            print("  Optimizer Parameters:")
            for key, val in best_result['optimizer_params'].items():
                print(f"    {key}: {val}")
        
        print(f"\n  Test Results:")
        print(f"    MAE: {best_result['test_results']['mae']:.6f}")
        print(f"    RMSE: {best_result['test_results']['rmse']:.6f}")
        print(f"    R²: {best_result['test_results']['r2_score']:.6f}")
        
        print(f"\n  Validation Results:")
        print(f"    MAE: {best_result['validation_results']['mae']:.6f}")
        print(f"    RMSE: {best_result['validation_results']['rmse']:.6f}")
        print(f"    R²: {best_result['validation_results']['r2_score']:.6f}")
        
        print(f"\n{'='*80}\n")
        
        # Comparison table
        print("ALL CONFIGURATIONS COMPARISON (sorted by Test MAE):\n")
        sorted_results = sorted(self.results, key=lambda x: x['test_results']['mae'])
        
        print(f"{'ID':<4} {'Optimizer':<10} {'LR':<8} {'Batch':<6} {'Units':<6} {'Drop':<6} "
              f"{'Test_MAE':<10} {'Test_R2':<10} {'Val_MAE':<10}")
        print("-" * 90)
        
        for r in sorted_results:
            print(f"{r['config_id']:<4} "
                  f"{r['configuration']['optimizer']:<10} "
                  f"{r['configuration']['learning_rate']:<8.5f} "
                  f"{r['configuration']['batch_size']:<6} "
                  f"{r['configuration']['units']:<6} "
                  f"{r['configuration']['dropout']:<6.2f} "
                  f"{r['test_results']['mae']:<10.6f} "
                  f"{r['test_results']['r2_score']:<10.6f} "
                  f"{r['validation_results']['mae']:<10.6f}")
        
        print("\n" + "="*80 + "\n")


def main():
    """Main hyperparameter tuning experiment"""
    
    print("\n" + "="*80)
    print("HYPERPARAMETER TUNING FOR DISEASE OUTBREAK FORECASTING")
    print("="*80 + "\n")
    
    # Choose disease and model type
    disease = 'Dengue'  # Can be changed to 'Typhoid' or 'Leptospirosis'
    model_type = 'LSTM'  # Can be 'LSTM' or 'GRU'
    
    print(f"Disease: {disease}")
    print(f"Model Type: {model_type}")
    print(f"Current Baseline Optimizer: Adam\n")
    
    # Define hyperparameter configurations to test
    configurations = [
        # BASELINE: Current configuration
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # Adam with different learning rates
        {
            'optimizer': 'Adam',
            'learning_rate': 0.01,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'Adam',
            'learning_rate': 0.0001,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # Adam with different beta values
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'beta_1': 0.95,
            'beta_2': 0.999,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # RMSprop optimizer
        {
            'optimizer': 'RMSprop',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'RMSprop',
            'learning_rate': 0.01,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'RMSprop',
            'learning_rate': 0.0001,
            'rho': 0.95,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # SGD optimizer
        {
            'optimizer': 'SGD',
            'learning_rate': 0.01,
            'momentum': 0.0,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'SGD',
            'learning_rate': 0.01,
            'momentum': 0.9,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'SGD',
            'learning_rate': 0.001,
            'momentum': 0.9,
            'nesterov': True,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # Different batch sizes with best optimizer
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 16,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 64,
            'units': 64,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # Different units
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 128,
            'dropout': 0.2,
            'epochs': 100,
        },
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 32,
            'dropout': 0.2,
            'epochs': 100,
        },
        
        # Different dropout rates
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.3,
            'epochs': 100,
        },
        {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'batch_size': 32,
            'units': 64,
            'dropout': 0.1,
            'epochs': 100,
        },
    ]
    
    print(f"Total Configurations to Test: {len(configurations)}\n")
    
    # Run tuning
    tuner = HyperparameterTuner(disease=disease, model_type=model_type)
    tuner.run_tuning(configurations)
    
    print("\n" + "="*80)
    print("HYPERPARAMETER TUNING COMPLETE!")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
