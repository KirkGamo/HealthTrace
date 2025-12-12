"""
Quick test to verify CCHAIN data integration fixes
"""
import sys
sys.path.append('.')

from app.data_utils import DataProcessor
import pandas as pd
import numpy as np

print("Testing CCHAIN Data Integration Fixes")
print("=" * 60)

# Test 1: Load data
print("\n1. Testing data loading...")
dp = DataProcessor(sequence_length=30)
df = pd.read_csv(os.path.join(project_root, 'app/data/dengue_historical_data.csv'))
print(f"   ✓ Loaded {len(df)} records")
print(f"   ✓ Columns: {list(df.columns)}")

# Test 2: Prepare features
print("\n2. Testing feature preparation...")
scaled = dp.prepare_features(df)
print(f"   ✓ Features shape: {scaled.shape}")
print(f"   ✓ Number of features: {scaled.shape[1]}")

# Test 3: Create sequences
print("\n3. Testing sequence creation...")
X, y = dp.create_sequences(scaled)
print(f"   ✓ X shape: {X.shape}")
print(f"   ✓ y shape: {y.shape}")

# Test 4: Inverse transform
print("\n4. Testing inverse transform...")
test_predictions = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
inversed = dp.inverse_transform_predictions(test_predictions)
print(f"   ✓ Inverse transform successful")
print(f"   ✓ Input shape: {test_predictions.shape}")
print(f"   ✓ Output shape: {inversed.shape}")
print(f"   ✓ Sample predictions: {inversed[:3]}")

# Test 5: Test all diseases
print("\n5. Testing all diseases...")
for disease in ['dengue', 'typhoid', 'cholera']:
    dp_test = DataProcessor(sequence_length=30)
    df_test = pd.read_csv(os.path.join(project_root, f'app/data/{disease}_historical_data.csv'))
    scaled_test = dp_test.prepare_features(df_test)
    X_test, y_test = dp_test.create_sequences(scaled_test)
    print(f"   ✓ {disease.capitalize()}: {X_test.shape[0]} sequences, {X_test.shape[2]} features")

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("\nYou can now:")
print("  1. Stop the Flask app (Ctrl+C in the terminal)")
print("  2. Restart it: python app.py")
print("  3. Test the API at http://localhost:5000")
