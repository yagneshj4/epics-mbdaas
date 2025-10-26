"""
Dormant Account Detection - Real Use Case #3 from MBDAaaS Paper
Detects inactive accounts that suddenly become active (security risk)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipelines.bootstrap_pipeline import BootstrapPipeline
from pipelines.detection_pipeline import DetectionPipeline

class DormantAccountDetector:
    def __init__(self):
        self.bootstrap = BootstrapPipeline()
        self.detector = DetectionPipeline(contamination=0.02)
        print("Dormant Account Detector Initialized")
    
    def generate_account_activity_logs(self, num_accounts=500):
        """Generate realistic account activity logs with dormant accounts"""
        from faker import Faker
        fake = Faker()
        
        data = []
        for i in range(num_accounts):
            # 10% chance of dormant account
            is_dormant = np.random.random() < 0.1
            
            if is_dormant:
                # Dormant: No activity for 6+ months, then sudden activity
                last_activity = datetime.now() - timedelta(days=np.random.randint(180, 720))
                current_activity = datetime.now()
                days_inactive = (current_activity - last_activity).days
            else:
                # Active: Regular activity
                last_activity = datetime.now() - timedelta(days=np.random.randint(1, 30))
                current_activity = datetime.now()
                days_inactive = (current_activity - last_activity).days
            
            record = {
                'account_id': fake.uuid4(),
                'user_name': fake.name(),
                'email': fake.email(),
                'last_login': last_activity,
                'current_login': current_activity,
                'days_inactive': days_inactive,
                'login_count_last_month': 0 if is_dormant else np.random.randint(5, 50),
                'data_accessed_mb': np.random.randint(1000, 10000) if is_dormant else np.random.randint(1, 100),
                'actions_performed': np.random.randint(50, 500) if is_dormant else np.random.randint(1, 20),
                'ip_address': fake.ipv4(),
                'user_agent': fake.user_agent(),
                'is_dormant': 1 if is_dormant else 0
            }
            data.append(record)
        
        return pd.DataFrame(data)
    
    def run_detection(self):
        """Run complete dormant account detection"""
        print("="*80)
        print("DORMANT ACCOUNT DETECTION - Real Security Use Case")
        print("="*80)
        
        # Step 1: Generate account logs
        print("\n[1/4] Generating Account Activity Logs...")
        logs = self.generate_account_activity_logs(500)
        logs.to_csv('data/raw/account_activity_logs.csv', index=False)
        print(f"Generated {len(logs)} account records")
        print(f"Dormant accounts: {logs['is_dormant'].sum()}")
        
        # Step 2: Anonymize
        print("\n[2/4] Anonymizing Account Data...")
        anonymized = self.bootstrap.anonymize_dataset(
            'data/raw/account_activity_logs.csv',
            'data/anonymized/accounts_anonymized.csv'
        )
        
        # Step 3: Detect dormant accounts
        print("\n[3/4] Detecting Dormant Account Activities...")
        results = self.detector.run_detection(
            'data/anonymized/accounts_anonymized.csv',
            'experiments/dormant_accounts/dormant_results.csv'
        )
        
        # Step 4: Analysis
        print("\n[4/4] Generating Analysis Report...")
        dormant_detected = results[results['is_anomaly'] == 1]
        
        print(f"\n{'='*80}")
        print("DORMANT ACCOUNT DETECTION RESULTS")
        print(f"{'='*80}")
        print(f"Total Accounts Analyzed: {len(results)}")
        print(f"Dormant Accounts Detected: {len(dormant_detected)}")
        print(f"Detection Rate: {len(dormant_detected)/len(results)*100:.2f}%")
        
        # Ground truth comparison
        actual_dormant = logs[logs['is_dormant'] == 1]
        print(f"Actual Dormant (Ground Truth): {len(actual_dormant)}")
        
        # Calculate precision
        accuracy = (results['is_anomaly'] == logs['is_dormant']).mean() * 100
        print(f"Detection Accuracy: {accuracy:.2f}%")
        
        print(f"\nResults saved to: experiments/dormant_accounts/dormant_results.csv")
        print(f"{'='*80}")
        
        return results

if __name__ == "__main__":
    detector = DormantAccountDetector()
    detector.run_detection()
