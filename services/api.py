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
    version="1.0.0"
)

class AnonymizeRequest(BaseModel):
    input_path: str
    output_path: str

class DetectionRequest(BaseModel):
    input_path: str
    output_path: str
    contamination: float = 0.1

@app.get("/'^)
async def root():
    return {
        "service": "EPICS MBDAaaS",
        "status": "running",
        "version": "1.0.0"
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
            "output_path": request.output_path
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
            "output_path": request.output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "MBDAaaS"}
