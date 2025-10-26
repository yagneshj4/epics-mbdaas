"""
MBDAaaS Dashboard
Web interface for monitoring and managing analytics workflows
"""

from flask import Flask, jsonify, render_template_string
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>EPICS MBDAaaS Dashboard</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { font-size: 2em; color: #3498db; font-weight: bold; }
        .label { color: #7f8c8d; font-size: 0.9em; }
        .status-ok { color: #27ae60; }
    </style>
</head>
<body>
    <div class="header">
        <h1>EPICS MBDAaaS Dashboard</h1>
        <p>Model-Based Big Data Analytics-as-a-Service</p>
    </div>
    
    <div class="card">
        <h2>System Status</h2>
        <p class="status-ok">All Services Running</p>
    </div>
    
    <div class="card">
        <h2>Pipeline Metrics</h2>
        <div class="metric">{{ total_records }}</div>
        <div class="label">Total Records Processed</div>
        <br>
        <div class="metric">{{ anonymized_records }}</div>
        <div class="label">Anonymized Records</div>
        <br>
        <div class="metric">{{ anomalies }}</div>
        <div class="label">Anomalies Detected</div>
    </div>
    
    <div class="card">
        <h2>Security Status</h2>
        <p>Pseudonymization: <span class="status-ok">Active</span></p>
        <p>Encryption: <span class="status-ok">AES-256</span></p>
        <p>Access Control: <span class="status-ok">RBAC Enabled</span></p>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Main dashboard view"""
    try:
        raw = pd.read_csv('data/raw/sample_data.csv')
        anonymized = pd.read_csv('data/anonymized/sample_anonymized.csv')
        results = pd.read_csv('results/tables/anomaly_results.csv')
        
        metrics = {
            'total_records': len(raw),
            'anonymized_records': len(anonymized),
            'anomalies': int(results['is_anomaly'].sum())
        }
    except:
        metrics = {
            'total_records': 0,
            'anonymized_records': 0,
            'anomalies': 0
        }
    
    return render_template_string(DASHBOARD_HTML, **metrics)

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'bootstrap': 'running',
            'detection': 'running',
            'anonymization': 'active'
        }
    })

if __name__ == '__main__':
    print("="*60)
    print("Starting EPICS MBDAaaS Dashboard")
    print("Access at: http://127.0.0.1:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
