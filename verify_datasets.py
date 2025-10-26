"""
Verify 3 Real Datasets are properly loaded
"""

import pandas as pd
from pathlib import Path

def verify_datasets():
    print("="*80)
    print("EPICS MBDAaaS - Dataset Verification")
    print("="*80)
    
    datasets = {
        'Dataset 1: Cybersecurity Logs': 'data/raw/cybersecurity/cybersecurity_threat_detection_logs.csv',
        'Dataset 2: Login Behavior (RBA)': 'data/raw/login_behavior/rba-dataset.csv',
        'Dataset 3: Smart Grid': 'data/raw/smart_grid/smart_grid_dataset.csv'
    }
    
    all_good = True
    
    for name, path in datasets.items():
        print(f"\n{name}")
        print("-" * 80)
        
        if Path(path).exists():
            df = pd.read_csv(path, nrows=5)
            print(f"✅ FOUND: {path}")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Shape: {df.shape}")
            print(f"   Preview:\n{df.head(2)}")
        else:
            print(f"❌ NOT FOUND: {path}")
            all_good = False
    
    print("\n" + "="*80)
    if all_good:
        print("✅ ALL 3 DATASETS VERIFIED AND READY!")
    else:
        print("⚠️  Some datasets are missing. Please check.")
    print("="*80)

if __name__ == "__main__":
    verify_datasets()
