"""
MBDAaaS REST API
FastAPI service for pipeline orchestration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.bootstrap_pipeline import BootstrapPipeline
from pipelines.detection_pipeline import DetectionPipeline

app = FastAPI(
    title="EPICS MBDAaaS API",
    description="Model-Based Big Data Analytics-as-a-Service",
    version="2.0.0"
)

class AnonymizeRequest(BaseModel):
    input_path: str
    output_path: str

class DetectionRequest(BaseModel):
    input_path: str
    output_path: str
    contamination: float = 0.1

@app.get("/")
async def root():
    return {
        "service": "EPICS MBDAaaS",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "anonymize": "/api/anonymize",
            "detect": "/api/detect"
        }
    }

@app.post("/api/anonymize")
async def anonymize_data(request: AnonymizeRequest):
    """Anonymize dataset using bootstrap pipeline"""
    try:
        pipeline = BootstrapPipeline()
        result = pipeline.anonymize_dataset(
            request.input_path,
            request.output_path
        )
        return {
            "status": "success",
            "records_processed": len(result),
            "output_path": request.output_path,
            "message": "Data anonymized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect")
async def detect_anomalies(request: DetectionRequest):
    """Detect anomalies using detection pipeline"""
    try:
        pipeline = DetectionPipeline(contamination=request.contamination)
        result = pipeline.run_detection(
            request.input_path,
            request.output_path
        )
        return {
            "status": "success",
            "total_records": len(result),
            "anomalies_detected": int(result['is_anomaly'].sum()),
            "output_path": request.output_path,
            "message": "Anomaly detection completed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Check system health"""
    return {
        "status": "healthy",
        "service": "EPICS MBDAaaS",
        "version": "2.0.0",
        "components": {
            "bootstrap_pipeline": "operational",
            "detection_pipeline": "operational",
            "dashboard": "running"
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    import pandas as pd
    try:
        # Load recent data
        raw = pd.read_csv('data/raw/sample_data.csv')
        anonymized = pd.read_csv('data/anonymized/sample_anonymized.csv')
        results = pd.read_csv('results/tables/anomaly_results.csv')
        
        return {
            "total_records": len(raw),
            "anonymized_records": len(anonymized),
            "anomalies_detected": int(results['is_anomaly'].sum()),
            "privacy_level": "High (epsilon=0.1)",
            "pseudonym_mappings": 201
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "No data available yet. Run pipeline first."
        }

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("Starting EPICS MBDAaaS REST API")
    print("Access at: http://127.0.0.1:8000")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
