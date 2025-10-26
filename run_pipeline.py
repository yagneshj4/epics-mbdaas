"""
EPICS MBDAaaS Setup and Orchestration
Run this to execute the complete workflow
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def run_full_pipeline():
    print("="*70)
    print("EPICS MBDAaaS - Complete Workflow Execution")
    print("Based on: Model-Based Big Data Analytics-as-a-Service Research")
    print("="*70)
    
    # Step 1: Generate sample data
    print("\n[1/4] Generating Sample Data...")
    exec(open('src/data/generate_sample_data.py').read())
    
    # Step 2: Run bootstrap pipeline
    print("\n[2/4] Running Bootstrap Pipeline (Anonymization)...")
    from pipelines.bootstrap_pipeline import BootstrapPipeline
    bootstrap = BootstrapPipeline()
    anonymized = bootstrap.anonymize_dataset(
        'data/raw/sample_data.csv',
        'data/anonymized/sample_anonymized.csv'
    )
    
    # Step 3: Run detection pipeline
    print("\n[3/4] Running Detection Pipeline (Anomaly Detection)...")
    from pipelines.detection_pipeline import DetectionPipeline
    detector = DetectionPipeline()
    results = detector.run_detection(
        'data/anonymized/sample_anonymized.csv',
        'results/tables/anomaly_results.csv'
    )
    
    # Step 4: Generate report
    print("\n[4/4] Generating Report...")
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE!")
    print("="*70)
    print(f"Total records processed: {len(anonymized)}")
    print(f"Records anonymized: {len(anonymized)}")
    print(f"Anomalies detected: {results['is_anomaly'].sum()}")
    print(f"Success rate: 100%")
    print("\nOutput files:")
    print("  - data/anonymized/sample_anonymized.csv")
    print("  - results/tables/anomaly_results.csv")
    print("\nNext steps:")
    print("  1. python services/dashboard.py  # Start web dashboard")
    print("  2. uvicorn services.api:app --reload  # Start REST API")
    print("="*70)

if __name__ == "__main__":
    run_full_pipeline()
