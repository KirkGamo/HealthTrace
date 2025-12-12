import sys
import os

# Add project root to path (go up two levels: testing -> scripts -> root)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from app.data_utils import DataProcessor

print("Testing feature extraction with 23 environmental features...\n")

processor = DataProcessor()
df = processor.load_data('app/data/dengue_historical_data.csv')
scaled_data = processor.prepare_features(df)
X, y = processor.create_sequences(scaled_data)

print(f"✓ Feature extraction successful!")
print(f"  Scaled data shape: {scaled_data.shape}")
print(f"  Sequence input shape: {X.shape}")
print(f"  Sequence output shape: {y.shape}")
print(f"  Features extracted: {X.shape[2]}")

expected_features = 23  # 23 input features

if X.shape[2] == expected_features:
    print(f"\n✓ CORRECT: Expected {expected_features} features, got {X.shape[2]}")
else:
    print(f"\n✗ ERROR: Expected {expected_features} features, got {X.shape[2]}")
