import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_utils import DataProcessor
from app.model import DiseaseOutbreakModel
from config import Config

def train_model(disease='Dengue', model_type='LSTM'):
    """Train disease outbreak forecasting model"""
    
    print(f"Training {model_type} model for {disease} outbreak forecasting...")
    
    # Initialize data processor
    data_processor = DataProcessor(sequence_length=Config.SEQUENCE_LENGTH)
    
    # Data file path
    data_file = os.path.join(Config.DATA_PATH, f'{disease.lower()}_historical_data.csv')
    
    # Check if data exists, if not prompt to run data preparation
    if not os.path.exists(data_file):
        print(f"ERROR: Data file not found: {data_file}")
        print(f"Please run 'python prepare_cchain_data.py' first to process CCHAIN data.")
        raise FileNotFoundError(f"Missing data file: {data_file}")
    
    # Load and prepare data
    print("Loading data...")
    df = data_processor.load_data(data_file)
    
    print("Preparing features...")
    scaled_data = data_processor.prepare_features(df)
    
    print("Creating sequences...")
    X, y = data_processor.create_sequences(scaled_data)
    
    print(f"Data shape: X={X.shape}, y={y.shape}")
    
    # Split data into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, shuffle=False  # Don't shuffle to maintain temporal order
    )
    
    print(f"Train shape: X={X_train.shape}, y={y_train.shape}")
    print(f"Validation shape: X={X_val.shape}, y={y_val.shape}")
    
    # Initialize and build model
    print(f"Building {model_type} model...")
    model = DiseaseOutbreakModel(
        sequence_length=Config.SEQUENCE_LENGTH,
        n_features=X.shape[2],
        model_type=model_type
    )
    model.build_model(units=64)
    
    print(model.model.summary())
    
    # Train model
    print("Training model...")
    model_dir = os.path.join(os.path.dirname(__file__), 'app', 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f'{disease.lower()}_forecast_model.h5')
    
    history = model.train(
        X_train, y_train,
        X_val, y_val,
        epochs=50,
        batch_size=32,
        model_path=model_path
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    train_loss, train_mae = model.model.evaluate(X_train, y_train)
    val_loss, val_mae = model.model.evaluate(X_val, y_val)
    
    print(f"Training - Loss: {train_loss:.4f}, MAE: {train_mae:.4f}")
    print(f"Validation - Loss: {val_loss:.4f}, MAE: {val_mae:.4f}")
    
    print(f"\nModel saved to: {model_path}")
    print("Training complete!")
    
    return model, history

if __name__ == '__main__':
    # Train models for diseases available in CCHAIN data
    diseases = Config.DISEASES  # ['Dengue', 'Typhoid', 'Cholera']
    
    print("\n" + "="*60)
    print("HEALTHTRACE MODEL TRAINING - CCHAIN DATA")
    print("Location: Iloilo City, Philippines")
    print(f"Diseases: {', '.join(diseases)}")
    print("="*60)
    
    for disease in diseases:
        print(f"\n{'='*60}")
        print(f"Training model for {disease}")
        print(f"{'='*60}\n")
        
        try:
            train_model(disease=disease, model_type='LSTM')
        except FileNotFoundError as e:
            print(f"\n{e}")
            print("\nPlease run: python prepare_cchain_data.py")
            break
        except Exception as e:
            print(f"Error training model for {disease}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n" + "="*60)
    print("Model training complete!")
    print("="*60)
