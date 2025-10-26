"""
Real-Time System Performance Monitor
Monitors pipeline performance, privacy budget, and system health
"""

import psutil
import time
from datetime import datetime
import pandas as pd

class SystemMonitor:
    def __init__(self):
        self.metrics = []
        print("System Monitor Started")
    
    def collect_metrics(self):
        """Collect real-time system metrics"""
        return {
            'timestamp': datetime.now(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.Process().memory_percent(),
            'disk_usage': psutil.disk_usage('/').percent,
            'active_threads': psutil.Process().num_threads()
        }
    
    def monitor_pipeline_execution(self, duration=10):
        """Monitor system during pipeline execution"""
        print(f"Monitoring system for {duration} seconds...")
        
        for i in range(duration):
            metrics = self.collect_metrics()
            self.metrics.append(metrics)
            print(f"[{i+1}/{duration}] CPU: {metrics['cpu_percent']}% | Memory: {metrics['memory_percent']:.2f}%")
            time.sleep(1)
        
        # Save metrics
        df = pd.DataFrame(self.metrics)
        df.to_csv('monitoring/performance/metrics.csv', index=False)
        print(f"\nMetrics saved to: monitoring/performance/metrics.csv")
        
        return df

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.monitor_pipeline_execution(10)
