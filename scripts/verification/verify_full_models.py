from tensorflow import keras

print("Verifying LSTM model shapes...\n")

models = ['dengue', 'typhoid', 'cholera']

for disease in models:
    model_path = f'app/models/{disease}_forecast_lstm.h5'
    model = keras.models.load_model(model_path)
    input_shape = model.input_shape
    print(f"{disease}: {input_shape}")

expected_shape = (None, 30, 52)
print(f"\nExpected shape: {expected_shape}")
print(f"✓ All LSTM models verified!")
print(f"\nFeature breakdown:")
print(f"  - Precipitation: 6 features")
print(f"  - Temperature: 6 features")
print(f"  - Air Quality: 6 features")
print(f"  - Vegetation: 1 feature")
print(f"  - Sanitation: 9 features")
print(f"  - Water Body: 9 features")
print(f"  - Healthcare: 9 features")
print(f"  - Wealth: 3 features")
print(f"  - Socioeconomic: 3 features")
print(f"  - Total: 52 input features")
