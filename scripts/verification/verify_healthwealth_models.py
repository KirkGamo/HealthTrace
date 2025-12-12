import numpy as np
from tensorflow import keras

print("Verifying model input shapes after healthcare/wealth feature addition...\n")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    model_path = f'app/models/{disease}_forecast_lstm.h5'
    print(f"\n{'='*60}")
    print(f"Loading {disease} LSTM model...")
    print(f"{'='*60}")
    
    model = keras.models.load_model(model_path)
    
    print(f"\nModel: {model_path}")
    print(f"Expected input shape: (None, 30, 52)")
    print(f"Actual input shape: {model.input_shape}")
    
    if model.input_shape == (None, 30, 52):
        print("✓ Model input shape is CORRECT")
    else:
        print("✗ WARNING: Model input shape mismatch!")
    
    print(f"\nTotal parameters: {model.count_params():,}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
print("\n✓ All models should have input shape (None, 30, 52)")
print("  - 30: sequence length (days)")
print("  - 52: features (41 existing + 11 healthcare/wealth)")
print("\nFeature breakdown:")
print("  - Climate: 6 (precipitation + indices)")
print("  - Socioeconomic: 3 (population + nighttime lights)")
print("  - Temperature: 6 (min/max/avg + ranges)")
print("  - Air quality: 6 (NO2, CO, SO2, O3, PM10, PM2.5)")
print("  - Vegetation: 1 (NDVI)")
print("  - Sanitation: 10 (water access, toilets, waste)")
print("  - Water bodies: 8 (proximity to wetlands, rivers, etc.)")
print("  - Healthcare: 8 (clinics, hospitals, pharmacies, doctors)")
print("  - Wealth: 3 (relative wealth index mean/median/std)")
print("  - Target: 1 (disease_cases)")
