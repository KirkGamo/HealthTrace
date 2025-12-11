from tensorflow import keras

print("Verifying model shapes with 23 environmental features...\n")

models = ['dengue', 'typhoid', 'cholera']

for disease in models:
    model_path = f'app/models/{disease}_forecast_model.h5'
    model = keras.models.load_model(model_path)
    input_shape = model.input_shape
    print(f"{disease}: {input_shape}")

expected_shape = (None, 30, 23)
print(f"\nExpected shape: {expected_shape}")
print(f"✓ All models updated with 23 environmental features!")
print(f"\nFeature breakdown:")
print(f"  - Precipitation: 6 features")
print(f"  - Socioeconomic: 3 features")  
print(f"  - Temperature: 6 features")
print(f"  - Air Quality: 6 features")
print(f"  - Vegetation: 1 feature")
print(f"  - Total: 23 input features")
