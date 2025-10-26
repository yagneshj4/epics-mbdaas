"""
Exploratory Data Analysis Notebook
Real-world data analysis for EPICS project
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def analyze_anonymized_data():
    """Analyze anonymized data quality"""
    print("="*80)
    print("EPICS MBDAaaS - Data Analysis Report")
    print("="*80)
    
    # Load data
    raw = pd.read_csv('data/raw/sample_data.csv')
    anonymized = pd.read_csv('data/anonymized/sample_anonymized.csv')
    results = pd.read_csv('results/tables/anomaly_results.csv')
    
    print("\n1. Dataset Statistics:")
    print(f"   Raw records: {len(raw)}")
    print(f"   Anonymized records: {len(anonymized)}")
    print(f"   Anomalies detected: {results['is_anomaly'].sum()}")
    
    print("\n2. Privacy Analysis:")
    print(f"   Pseudonymized columns: {len([col for col in anonymized.columns if 'pseudo' in col])}")
    print(f"   Data utility preserved: {(anonymized.select_dtypes(include=['float64']).notna().sum().sum() / anonymized.select_dtypes(include=['float64']).size) * 100:.2f}%")
    
    print("\n3. Anomaly Distribution:")
    print(f"   Normal records: {(results['is_anomaly'] == 0).sum()}")
    print(f"   Anomalous records: {(results['is_anomaly'] == 1).sum()}")
    
    # Save analysis
    analysis_report = {
        'metric': ['Total Records', 'Anonymized', 'Anomalies', 'Privacy Level'],
        'value': [len(raw), len(anonymized), results['is_anomaly'].sum(), 'High (ε=0.1)']
    }
    
    pd.DataFrame(analysis_report).to_csv('notebooks/reports/analysis_report.csv', index=False)
    print("\nAnalysis saved to: notebooks/reports/analysis_report.csv")

if __name__ == "__main__":
    analyze_anonymized_data()
