import numpy as np
from tensorflow import keras

print("Verifying model input shapes after sanitation/water body feature addition...\n")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    model_path = f'app/models/{disease}_forecast_lstm.h5'
    print(f"\n{'='*60}")
    print(f"Loading {disease} model...")
    print(f"{'='*60}")
    
    model = keras.models.load_model(model_path)
    
    print(f"\nModel: {model_path}")
    print(f"Expected input shape: (None, 30, 41)")
    print(f"Actual input shape: {model.input_shape}")
    
    if model.input_shape == (None, 30, 41):
        print("✓ Model input shape is CORRECT")
    else:
        print("✗ WARNING: Model input shape mismatch!")
    
    print(f"\nTotal parameters: {model.count_params():,}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
print("\n✓ All models should have input shape (None, 30, 41)")
print("  - 30: sequence length (days)")
print("  - 41: features (23 environmental + 18 sanitation/water body)")
