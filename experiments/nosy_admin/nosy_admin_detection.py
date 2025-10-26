"""
Nosy Admin Detection - Real Use Case from MBDAaaS Paper
Detects database administrators accessing sensitive customer data without authorization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipelines.bootstrap_pipeline import BootstrapPipeline
from pipelines.detection_pipeline import DetectionPipeline

class NosyAdminDetector:
    def __init__(self):
        self.bootstrap = BootstrapPipeline()
        self.detector = DetectionPipeline(contamination=0.05)
        print("Nosy Admin Detector Initialized")
    
    def generate_admin_access_logs(self, num_records=1000):
        """Generate realistic database admin access logs"""
        from faker import Faker
        fake = Faker()
        
        # Normal admin activities
        normal_activities = ['backup', 'schema_update', 'index_optimization', 'health_check']
        # Suspicious activities
        suspicious_activities = ['customer_table_scan', 'credit_card_query', 'email_export', 'bulk_data_download']
        
        data = []
        for i in range(num_records):
            is_suspicious = np.random.random() < 0.05  # 5% suspicious
            
            record = {
                'admin_id': fake.uuid4(),
                'admin_name': fake.name(),
                'timestamp': datetime.now() - timedelta(hours=np.random.randint(0, 720)),
                'database': np.random.choice(['customers_db', 'orders_db', 'products_db', 'analytics_db']),
                'table_accessed': np.random.choice(['users', 'orders', 'payments', 'products', 'sessions']),
                'operation': np.random.choice(suspicious_activities if is_suspicious else normal_activities),
                'rows_accessed': np.random.randint(1, 100000) if is_suspicious else np.random.randint(1, 1000),
                'access_duration_seconds': np.random.randint(300, 3600) if is_suspicious else np.random.randint(1, 300),
                'ip_address': fake.ipv4(),
                'is_after_hours': np.random.choice([True, False]),
                'label': 1 if is_suspicious else 0  # Ground truth for evaluation
            }
            data.append(record)
        
        df = pd.DataFrame(data)
        return df
    
    def run_detection(self):
        """Run complete nosy admin detection pipeline"""
        print("="*80)
        print("NOSY ADMIN DETECTION - Real Use Case Implementation")
        print("="*80)
        
        # Step 1: Generate realistic admin access logs
        print("\n[1/4] Generating Admin Access Logs...")
        logs = self.generate_admin_access_logs(1000)
        logs.to_csv('data/raw/admin_access_logs.csv', index=False)
        print(f"Generated {len(logs)} admin access records")
        
        # Step 2: Anonymize admin identities (privacy protection)
        print("\n[2/4] Anonymizing Admin Identities...")
        anonymized = self.bootstrap.anonymize_dataset(
            'data/raw/admin_access_logs.csv',
            'data/anonymized/admin_access_anonymized.csv'
        )
        
        # Step 3: Detect nosy admin behavior
        print("\n[3/4] Detecting Suspicious Admin Behavior...")
        results = self.detector.run_detection(
            'data/anonymized/admin_access_anonymized.csv',
            'experiments/nosy_admin/nosy_admin_results.csv'
        )
        
        # Step 4: Generate report
        print("\n[4/4] Generating Detection Report...")
        suspicious = results[results['is_anomaly'] == 1]
        print(f"\n{'='*80}")
        print(f"DETECTION RESULTS")
        print(f"{'='*80}")
        print(f"Total Admin Activities: {len(results)}")
        print(f"Suspicious Activities Detected: {len(suspicious)}")
        print(f"Detection Rate: {len(suspicious)/len(results)*100:.2f}%")
        
        # Compare with ground truth
        if 'label' in logs.columns:
            actual_suspicious = logs[logs['label'] == 1]
            print(f"Actual Suspicious (Ground Truth): {len(actual_suspicious)}")
            accuracy = (results['is_anomaly'] == logs['label']).mean() * 100
            print(f"Detection Accuracy: {accuracy:.2f}%")
        
        print(f"\nResults saved to: experiments/nosy_admin/nosy_admin_results.csv")
        print(f"{'='*80}")
        
        return results

if __name__ == "__main__":
    detector = NosyAdminDetector()
    detector.run_detection()
