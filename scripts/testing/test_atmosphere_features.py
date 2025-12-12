from app.data_utils import DataProcessor

print("Testing feature extraction with atmosphere features...\n")

processor = DataProcessor()
df = processor.load_data(os.path.join(project_root, 'app/data/dengue_historical_data.csv'))
scaled_data = processor.prepare_features(df)
X, y = processor.create_sequences(scaled_data)

print(f"✓ Feature extraction successful!")
print(f"  Scaled data shape: {scaled_data.shape}")
print(f"  Sequence input shape: {X.shape}")
print(f"  Sequence output shape: {y.shape}")
print(f"  Features extracted: {X.shape[2]}")

expected_features = 16  # 16 input features

if X.shape[2] == expected_features:
    print(f"\n✓ CORRECT: Expected {expected_features} features, got {X.shape[2]}")
else:
    print(f"\n✗ ERROR: Expected {expected_features} features, got {X.shape[2]}")
