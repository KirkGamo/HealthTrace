import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

class DiseaseOutbreakModel:
    """LSTM/GRU model for disease outbreak forecasting"""
    
    def __init__(self, sequence_length=30, n_features=4, model_type='LSTM'):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model_type = model_type
        self.model = None
        
    def build_model(self, units=64, dropout=0.3):
        """Build LSTM or GRU model architecture"""
        model = Sequential()
        
        if self.model_type == 'LSTM':
            # First LSTM layer with return sequences
            model.add(LSTM(units=units, return_sequences=True, 
                          input_shape=(self.sequence_length, self.n_features)))
            model.add(Dropout(dropout))
            
            # Second LSTM layer
            model.add(LSTM(units=units//2, return_sequences=False))
            model.add(Dropout(dropout))
            
        elif self.model_type == 'GRU':
            # First GRU layer with return sequences
            model.add(GRU(units=units, return_sequences=True,
                         input_shape=(self.sequence_length, self.n_features)))
            model.add(Dropout(dropout))
            
            # Second GRU layer
            model.add(GRU(units=units//2, return_sequences=False))
            model.add(Dropout(dropout))
        
        # Dense layers for output
        model.add(Dense(units=32, activation='relu'))
        model.add(Dropout(dropout))
        model.add(Dense(units=1))  # Output: predicted disease cases
        
        # Compile model
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32, model_path=None):
        """Train the model"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        ]
        
        if model_path:
            callbacks.append(
                ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True)
            )
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not built or loaded")
        
        predictions = self.model.predict(X)
        return predictions
    
    def predict_future(self, last_sequence, n_days=14):
        """Predict multiple days into the future"""
        predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(n_days):
            # Predict next day
            next_pred = self.model.predict(current_sequence.reshape(1, self.sequence_length, self.n_features), verbose=0)
            predictions.append(next_pred[0, 0])
            
            # Update sequence: remove first day, add prediction
            # For simplicity, we keep other features constant (could be improved with climate forecasts)
            new_row = current_sequence[-1].copy()
            new_row[-1] = next_pred[0, 0]  # Update disease cases
            
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        return np.array(predictions)
    
    def save_model(self, filepath):
        """Save model to file"""
        if self.model is None:
            raise ValueError("Model not built or loaded")
        
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model from file"""
        import tensorflow as tf
        # Use compile=False to avoid metrics deserialization issues
        self.model = tf.keras.models.load_model(filepath, compile=False)
        # Recompile with current metrics
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        print(f"Model loaded from {filepath}")
        return self.model
