from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import redis.asyncio as redis
from celery import Celery
import structlog
import os
from typing import Dict, Any

# Import routers
from .routes.partners import router as partners_router
from .routes.leads import router as leads_router
from .routes.Quantum Nexus import router as quantum_nexus_router
from .routes.stripe import router as stripe_router
from .routes.auth import router as auth_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Celery Configuration
celery_app = Celery(
    "quantum_nexus_engine",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "api.src.tasks.quantum_tasks",
        "api.src.tasks.lead_tasks",
        "api.src.tasks.partner_tasks",
        "api.src.tasks.analytics_tasks"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Global Redis connection
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events"""
    global redis_client
    
    # Startup
    logger.info("Starting Quantum Nexus Engine API")
    
    # Initialize Redis connection
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    
    # Test Redis connection
    try:
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error("Failed to connect to Redis", error=str(e))
        raise
    
    # Store Redis client in app state
    app.state.redis = redis_client
    app.state.celery = celery_app
    
    yield
    
    # Shutdown
    logger.info("Shutting down Quantum Nexus Engine API")
    if redis_client:
        await redis_client.close()

# FastAPI Application
app = FastAPI(
    title="Quantum Nexus Engine - Consolidated API",
    description="Enterprise-ready quantum-powered business intelligence platform with real-time processing",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://*.flyfox.ai",
        "https://*.quantumnexus.ai"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Comprehensive health check for all services"""
    health_status = {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": structlog.processors.TimeStamper(fmt="iso")(),
        "services": {}
    }
    
    # Check Redis
    try:
        await app.state.redis.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Celery workers
    try:
        inspect = app.state.celery.control.inspect()
        active_workers = inspect.active()
        if active_workers:
            health_status["services"]["celery"] = "healthy"
            health_status["services"]["active_workers"] = len(active_workers)
        else:
            health_status["services"]["celery"] = "no_workers"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["services"]["celery"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint"""
    # This would integrate with prometheus_client
    return {"message": "Metrics endpoint - integrate with Prometheus"}

# Real-time status endpoint
@app.get("/status/quantum-jobs")
async def quantum_jobs_status():
    """Get real-time status of quantum jobs"""
    try:
        # Get active quantum jobs from Redis
        active_jobs = await app.state.redis.keys("quantum:job:*")
        job_statuses = []
        
        for job_key in active_jobs:
            job_data = await app.state.redis.hgetall(job_key)
            job_statuses.append(job_data)
        
        return {
            "active_jobs": len(job_statuses),
            "jobs": job_statuses
        }
    except Exception as e:
        logger.error("Failed to get quantum job status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve job status")

# WebSocket endpoint for real-time updates
@app.websocket("/ws/quantum-updates")
async def websocket_quantum_updates(websocket):
    """WebSocket endpoint for real-time quantum job updates"""
    await websocket.accept()
    
    # Subscribe to Redis pub/sub for quantum updates
    pubsub = app.state.redis.pubsub()
    await pubsub.subscribe("quantum:updates")
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
    finally:
        await pubsub.unsubscribe("quantum:updates")
        await websocket.close()

# Include routers with enhanced middleware
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(partners_router, prefix="/api/partners", tags=["partners"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(quantum_nexus_router, prefix="/api/quantum-nexus-engine", tags=["quantum-nexus-engine"])
app.include_router(stripe_router, prefix="/api/billing", tags=["billing"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Quantum Nexus Engine - Consolidated API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Real-time quantum processing",
            "Distributed task queue",
            "WebSocket support",
            "Enterprise authentication",
            "Comprehensive monitoring"
        ],
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "quantum_status": "/status/quantum-jobs",
            "websocket": "/ws/quantum-updates"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_consolidated:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None  # Use structlog instead
    )