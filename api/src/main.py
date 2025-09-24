from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routes.partners import router as partners_router
from src.routes.leads import router as leads_router
from src.routes.qnexus import router as qnexus_router
from src.routes.diversegy import router as diversegy_router
from src.routes.auth import router as auth_router
from src.routes.aiprm import router as aiprm_router
from src.routes.entitlements import router as entitlements_router
from src.routes.security import router as security_router
# from src.routes.performance import router as performance_router
from src.routes.dynex import router as dynex_router
from src.routes.stripe import router as stripe_router
from src.routes.diversegy import router as diversegy_router
from src.routes.sigma_router import sigma_router
from src.security.middleware import SecurityMiddleware
import uvicorn
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
import sys
from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))
# from quantum.reasoning import reversal_reasoning_sync
from typing import Dict, Any

app = FastAPI(
    title="NQBA Quantum Sales API",
    description="Demo API for Quantum-Enhanced Sales Intelligence",
    version="1.0.0"
)

# Security middleware (should be added first)
# app.add_middleware(
#     SecurityMiddleware,
#     enable_rate_limiting=True,
#     enable_audit_logging=True,
#     enable_ip_filtering=True,
#     enable_compliance_checks=True
# )

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(partners_router, prefix="/api/partners", tags=["partners"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(diversegy_router, prefix="/api/diversegy", tags=["diversegy"])
app.include_router(qnexus_router, prefix="/api/quantum-nexus-engine", tags=["quantum-nexus-engine"])
app.include_router(aiprm_router, prefix="/api/aiprm", tags=["aiprm"])
app.include_router(stripe_router, prefix="/api", tags=["stripe"])
app.include_router(entitlements_router, prefix="/api", tags=["entitlements"])
app.include_router(security_router, prefix="/api/security", tags=["security"])
# app.include_router(performance_router, prefix="/api/performance", tags=["performance"])
app.include_router(dynex_router, prefix="/api/dynex", tags=["dynex"])
app.include_router(sigma_router, prefix="/api/sigma", tags=["sigma"])

# from quantum.quantum_job_manager import QuantumJobManager

from src.dynex_client import dynex_client
# from qdllm.core.nuco_client import NucoClient

# nuco_client = NucoClient("test_key")  # FLYFOX AI: Use environment variable for production

# @app.post("/api/compute/submit")
# async def submit_compute(payload: Dict[str, Any]):
#     manager = QuantumJobManager(dynex_client, nuco_client)
#     job_id = manager.submit_job(payload)
#     return {"job_id": job_id, "estimated_cost": "70% < AWS"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
        }
    )

@app.get("/")
async def root():
    return {
        "message": "NQBA Quantum Sales API",
        "version": "1.0.0",
        "status": "operational",
        "quantum_enhanced": True,
        "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "quantum_core": "operational",
        "dynex_simulation": "active",
        "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
    }

@app.websocket("/ws/qdllm-status")
async def qdllm_status_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Example status using reversal_reasoning
            await websocket.send_json({
                "type": "status_update",
                "data": {"status": "operational"}  # Placeholder since quantum.reasoning is unavailable
            })
            await asyncio.sleep(10)  # Update every 10 seconds
    except WebSocketDisconnect:
        print("WebSocket disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)