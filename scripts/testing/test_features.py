import sys
sys.path.append('.')
from app.data_utils import DataProcessor
import pandas as pd

dp = DataProcessor()
df = pd.read_csv(os.path.join(project_root, 'app/data/dengue_historical_data.csv'))
scaled = dp.prepare_features(df)

print('Feature preparation test:')
print(f'  Input columns: {len(df.columns)} (including date)')
print(f'  Features extracted: {scaled.shape[1]}')
print(f'  Expected: 10 (9 input + 1 target)')
print(f'  Status: {"✓ CORRECT" if scaled.shape[1] == 10 else "✗ WRONG"}')
