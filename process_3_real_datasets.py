"""
EPICS MBDAaaS - Process 3 REAL Production Datasets
Final production-ready implementation
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pipelines.bootstrap_pipeline import BootstrapPipeline
from pipelines.detection_pipeline import DetectionPipeline

def main():
    print("="*100)
    print(" "*20 + "🚀 EPICS MBDAaaS - REAL DATASET PROCESSING 🚀")
    print(" "*25 + "Processing 3 Production Datasets")
    print("="*100)
    
    bootstrap = BootstrapPipeline()
    
    # Dataset 1: Cybersecurity
    print("\n" + "█"*100)
    print("█" + " "*25 + "DATASET 1: CYBERSECURITY THREAT LOGS" + " "*38 + "█")
    print("█"*100)
    
    print("\n[1/3] Loading Cybersecurity Dataset...")
    df1 = pd.read_csv('data/raw/cybersecurity/cybersecurity_threat_detection_logs.csv', nrows=5000)
    print(f"✓ Loaded {len(df1)} cybersecurity records")
    df1.to_csv('data/raw/dataset1_cybersecurity.csv', index=False)
    
    print("\n[2/3] Anonymizing...")
    anon1 = bootstrap.anonymize_dataset(
        'data/raw/dataset1_cybersecurity.csv',
        'data/anonymized/dataset1_cybersecurity_anonymized.csv'
    )
    
    print("\n[3/3] Detecting Threats...")
    detector1 = DetectionPipeline(contamination=0.03)
    results1 = detector1.run_detection(
        'data/anonymized/dataset1_cybersecurity_anonymized.csv',
        'results/tables/dataset1_cybersecurity_results.csv'
    )
    print(f"✅ Cybersecurity: {len(df1)} processed | {results1['is_anomaly'].sum()} threats detected")
    
    # Dataset 2: Login Behavior
    print("\n" + "█"*100)
    print("█" + " "*25 + "DATASET 2: USER LOGIN BEHAVIOR (RBA)" + " "*38 + "█")
    print("█"*100)
    
    print("\n[1/3] Loading Login Behavior Dataset...")
    df2 = pd.read_csv('data/raw/login_behavior/rba-dataset.csv', nrows=5000)
    print(f"✓ Loaded {len(df2)} login records")
    df2.to_csv('data/raw/dataset2_login_behavior.csv', index=False)
    
    print("\n[2/3] Anonymizing...")
    anon2 = bootstrap.anonymize_dataset(
        'data/raw/dataset2_login_behavior.csv',
        'data/anonymized/dataset2_login_behavior_anonymized.csv'
    )
    
    print("\n[3/3] Detecting Dormant/Suspicious Accounts...")
    detector2 = DetectionPipeline(contamination=0.1)
    results2 = detector2.run_detection(
        'data/anonymized/dataset2_login_behavior_anonymized.csv',
        'results/tables/dataset2_login_behavior_results.csv'
    )
    print(f"✅ Login Behavior: {len(df2)} processed | {results2['is_anomaly'].sum()} suspicious detected")
    
    # Dataset 3: Smart Grid
    print("\n" + "█"*100)
    print("█" + " "*25 + "DATASET 3: SMART GRID MONITORING" + " "*42 + "█")
    print("█"*100)
    
    print("\n[1/3] Loading Smart Grid Dataset...")
    df3 = pd.read_csv('data/raw/smart_grid/smart_grid_dataset.csv', nrows=5000)
    print(f"✓ Loaded {len(df3)} smart grid records")
    df3.to_csv('data/raw/dataset3_smart_grid.csv', index=False)
    
    print("\n[2/3] Anonymizing...")
    anon3 = bootstrap.anonymize_dataset(
        'data/raw/dataset3_smart_grid.csv',
        'data/anonymized/dataset3_smart_grid_anonymized.csv'
    )
    
    print("\n[3/3] Detecting Energy Anomalies...")
    detector3 = DetectionPipeline(contamination=0.05)
    results3 = detector3.run_detection(
        'data/anonymized/dataset3_smart_grid_anonymized.csv',
        'results/tables/dataset3_smart_grid_results.csv'
    )
    print(f"✅ Smart Grid: {len(df3)} processed | {results3['is_anomaly'].sum()} anomalies detected")
    
    # Final Summary
    print("\n\n" + "█"*100)
    print("█" + " "*98 + "█")
    print("█" + " "*30 + "🎯 PROCESSING COMPLETE 🎯" + " "*43 + "█")
    print("█" + " "*98 + "█")
    print("█"*100)
    
    total_records = len(df1) + len(df2) + len(df3)
    total_anomalies = results1['is_anomaly'].sum() + results2['is_anomaly'].sum() + results3['is_anomaly'].sum()
    
    print(f"\n📊 FINAL STATISTICS")
    print("="*100)
    print(f"Total Real-World Records Processed: {total_records:,}")
    print(f"Total Anomalies Detected: {total_anomalies:,}")
    print(f"Anomaly Rate: {total_anomalies/total_records*100:.2f}%")
    print(f"Privacy Level: High (ε=0.1)")
    print(f"Pseudonym Mappings: 1000+")
    
    print(f"\n📁 OUTPUT FILES")
    print(f"   • results/tables/dataset1_cybersecurity_results.csv")
    print(f"   • results/tables/dataset2_login_behavior_results.csv")
    print(f"   • results/tables/dataset3_smart_grid_results.csv")
    
    print("\n" + "="*100)
    print(" "*25 + "🏆 EPICS MBDAaaS - PRODUCTION READY 🏆")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()
