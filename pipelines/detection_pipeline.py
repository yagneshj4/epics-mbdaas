"""
Detection Pipeline - Security Incident Detection
Implements anomaly detection for security threats
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from pathlib import Path

class DetectionPipeline:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        print("Detection Pipeline Initialized")

    def detect_anomalies(self, data):
        """Detect anomalies in data using Isolation Forest"""
        predictions = self.model.fit_predict(data)
        anomalies = np.where(predictions == -1)[0]
        return anomalies

    def run_detection(self, input_path, output_path):
        """Run anomaly detection pipeline"""
        print(f"Loading data from {input_path}...")
        df = pd.read_csv(input_path)
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        data = df[numeric_cols]
        
        # Detect anomalies
        anomalies = self.detect_anomalies(data)
        print(f"Detected {len(anomalies)} anomalies")
        
        # Mark anomalies
        df['is_anomaly'] = 0
        df.loc[anomalies, 'is_anomaly'] = 1
        
        # Save results
        df.to_csv(output_path, index=False)
        print(f"Detection results saved to {output_path}")
        return df

if __name__ == "__main__":
    pipeline = DetectionPipeline()
    print("Detection Pipeline Ready!")
