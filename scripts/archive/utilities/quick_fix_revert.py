"""
Quick Fix: Temporarily revert to 7-feature data to match existing models
Run this if you want to use the app immediately without retraining
"""

import shutil
from pathlib import Path
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = Path(project_root) / 'app' / 'data'
DISEASES = ['dengue', 'typhoid', 'cholera']

def revert_to_original():
    """Temporarily use original 7-feature data"""
    print("Reverting to 7-feature data (temporary fix)...")
    
    for disease in DISEASES:
        original = DATA_DIR / f'{disease}_historical_data_original.csv'
        enhanced = DATA_DIR / f'{disease}_historical_data_enhanced.csv'
        current = DATA_DIR / f'{disease}_historical_data.csv'
        
        if original.exists():
            # Backup enhanced version
            if enhanced.exists():
                print(f"  Enhanced version already backed up: {disease}")
            else:
                shutil.copy2(current, enhanced)
                print(f"  Backed up enhanced data: {disease}")
            
            # Restore original
            shutil.copy2(original, current)
            print(f"  ✓ Restored original 7-feature data: {disease}")

def main():
    print("="*60)
    print("TEMPORARY FIX: Reverting to 7-feature data")
    print("="*60)
    print()
    print("⚠ This is a temporary solution!")
    print("The app will work with existing models, but won't use")
    print("the new enhanced features (population, nighttime lights).")
    print()
    
    revert_to_original()
    
    print("\n" + "="*60)
    print("✓ Reverted to 7-feature data")
    print("="*60)
    print("\nThe app should now work with existing models.")
    print("\nTo use enhanced features properly:")
    print("  1. Retrain models: python train_model.py")
    print("  2. Re-activate enhanced data: python activate_enhanced_features.py")
    print("  3. Restart app: python app.py")

if __name__ == '__main__':
    main()
