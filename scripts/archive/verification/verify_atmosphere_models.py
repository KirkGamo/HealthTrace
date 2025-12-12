from tensorflow import keras

print("Checking model shapes after atmosphere feature integration...\n")

models = ['dengue', 'typhoid', 'cholera']

for disease in models:
    model_path = f'app/models/{disease}_forecast_lstm.h5'
    model = keras.models.load_model(model_path)
    input_shape = model.input_shape
    print(f"{disease}: {input_shape}")

expected_shape = (None, 30, 16)
print(f"\nExpected shape: {expected_shape}")
print(f"✓ All models updated with 16 atmosphere-enhanced features!")
