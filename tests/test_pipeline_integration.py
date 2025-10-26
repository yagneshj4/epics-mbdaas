"""
End-to-End Pipeline Test
Tests the complete MBDAaaS workflow
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.bootstrap_pipeline import BootstrapPipeline
from pipelines.detection_pipeline import DetectionPipeline

def main():
    print("="*60)
    print("EPICS MBDAaaS - End-to-End Pipeline Test")
    print("="*60)

    # Step 1: Anonymize data
    print("\n[1/2] Running Bootstrap Pipeline...")
    bootstrap = BootstrapPipeline()
    anonymized = bootstrap.anonymize_dataset(
        'data/raw/sample_data.csv',
        'data/anonymized/sample_anonymized.csv'
    )

    # Step 2: Detect anomalies
    print("\n[2/2] Running Detection Pipeline...")
    detector = DetectionPipeline()
    results = detector.run_detection(
        'data/anonymized/sample_anonymized.csv',
        'results/tables/anomaly_results.csv'
    )

    print("\n" + "="*60)
    print("Pipeline Test Complete!")
    print("="*60)
    print(f"Anonymized records: {len(anonymized)}")
    print(f"Anomalies detected: {results['is_anomaly'].sum()}")

if __name__ == "__main__":
    main()
