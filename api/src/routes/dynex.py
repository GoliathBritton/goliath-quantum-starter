from fastapi import APIRouter
from typing import Dict, Any
from src.dynex_client import dynex_client

router = APIRouter(prefix="/dynex", tags=["dynex"])

@router.post("/submit-job")
def submit_quantum_job(job_data: Dict[str, Any]):
    job_type = job_data.get("type")
    input_data = job_data.get("input_data", {})
    job_id = dynex_client.submit_quantum_job(job_type, input_data)
    return {"job_id": job_id, "status": "submitted"}

@router.get("/job/{job_id}")
def get_job_status(job_id: str):
    return dynex_client.get_job_status(job_id)

@router.post("/qnexus-predict")
def qnexus_predict(predict_data: Dict[str, Any]):
    query = predict_data.get("query")
    context = predict_data.get("context")
    result = dynex_client.qnexus_predict(query, context)
    return result

@router.get("/network-status")
def get_network_status():
    return dynex_client.get_network_status()