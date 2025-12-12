import sys
import os

# Add project root to path (go up two levels: testing -> scripts -> root)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from app.data_utils import DataProcessor
import pandas as pd

dp = DataProcessor()
df = pd.read_csv('app/data/dengue_historical_data.csv')
scaled = dp.prepare_features(df)

print('Feature preparation test:')
print(f'  Input columns: {len(df.columns)} (including date)')
print(f'  Features extracted: {scaled.shape[1]}')
print(f'  Expected: 10 (9 input + 1 target)')
print(f'  Status: {"✓ CORRECT" if scaled.shape[1] == 10 else "✗ WRONG"}')
