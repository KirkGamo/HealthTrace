"""
Verify that all reorganized scripts can import correctly
Run this from the project root to ensure imports work after reorganization
"""

import sys
import os
from pathlib import Path

# Test imports from different script locations
def test_imports():
    """Test that imports work from reorganized directories"""
    
    print("Testing imports after repository reorganization...\n")
    
    tests = [
        ("Testing scripts/utilities/hyperparameter_tuning.py", 
         "scripts.utilities.hyperparameter_tuning"),
        ("Testing scripts/verification/compare_models.py",
         "scripts.verification.compare_models"),
        ("Testing scripts/testing/test_app.py",
         "scripts.testing.test_app"),
        ("Testing scripts/testing/test_features.py",
         "scripts.testing.test_features"),
        ("Testing scripts/testing/test_fixes.py",
         "scripts.testing.test_fixes"),
    ]
    
    passed = 0
    failed = 0
    
    for description, module_name in tests:
        try:
            # Try to import the module
            __import__(module_name)
            print(f"✅ {description}")
            passed += 1
        except ImportError as e:
            # Check if it's a missing dependency (sklearn, tensorflow) vs path issue
            error_msg = str(e)
            if 'sklearn' in error_msg or 'tensorflow' in error_msg or 'pandas' in error_msg:
                print(f"⚠️  {description} - Missing dependency (OK): {error_msg}")
                passed += 1
            else:
                print(f"❌ {description} - Path issue: {error_msg}")
                failed += 1
        except Exception as e:
            print(f"❌ {description} - Error: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    
    if failed == 0:
        print("\n✅ All import paths are correctly configured!")
        print("Note: Some scripts may require dependencies (sklearn, tensorflow, pandas)")
        print("      but the import paths from the reorganized structure are working.")
        return 0
    else:
        print(f"\n❌ {failed} script(s) have path configuration issues")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
