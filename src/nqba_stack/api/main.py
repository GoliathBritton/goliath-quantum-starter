"""
NQBA Main API Application

FastAPI application with CORS, middleware, and router setup
for the NQBA ecosystem.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

from .business_units import router as business_units_router
from .high_council import router as high_council_router
from .monitoring import router as monitoring_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting NQBA API Server...")
    logger.info("Initializing business unit integration...")

    # Import and initialize business unit manager
    try:
        from ..business_integration import business_unit_manager
        from ..business_integration import FLYFOXAIBusinessUnit

        # Register FLYFOX AI business unit
        flyfox_ai = FLYFOXAIBusinessUnit()
        await business_unit_manager.register_business_unit(flyfox_ai)

        # Start monitoring
        await business_unit_manager.start_monitoring()

        logger.info("NQBA API Server started successfully")
        logger.info(
            f"Registered business units: {len(await business_unit_manager.get_all_business_units())}"
        )

    except Exception as e:
        logger.error(f"Failed to initialize business units: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down NQBA API Server...")
    try:
        await business_unit_manager.stop_monitoring()
        logger.info("Business unit monitoring stopped")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="NQBA (Neuromorphic Quantum Business Architecture) API",
    description="API for the NQBA ecosystem - FLYFOX AI, Goliath of All Trade, and Sigma Select",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # In production, restrict to specific hosts
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests"""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": time.time(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time(),
        },
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to NQBA (Neuromorphic Quantum Business Architecture) API",
        "version": "2.0.0",
        "description": "API for the NQBA ecosystem",
        "business_units": [
            "FLYFOX AI - Energy Optimization",
            "Goliath of All Trade - Financial Operations",
            "Sigma Select - Sales Intelligence",
        ],
        "documentation": "/docs",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from ..business_integration import business_unit_manager

        # Get ecosystem status
        ecosystem_status = await business_unit_manager.get_ecosystem_status()

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "ecosystem": ecosystem_status,
            "api_version": "2.0.0",
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e), "timestamp": time.time()}


@app.get("/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "NQBA API",
        "version": "2.0.0",
        "description": "Neuromorphic Quantum Business Architecture API",
        "business_units": {
            "flyfox_ai": {
                "name": "FLYFOX AI",
                "description": "Energy optimization and consumption management",
                "endpoints": "/api/v1/flyfox-ai",
                "quantum_advantage": "3.2x energy optimization",
            },
            "goliath_trade": {
                "name": "Goliath of All Trade",
                "description": "Financial trading and portfolio optimization",
                "endpoints": "/api/v1/goliath-trade",
                "quantum_advantage": "4.1x portfolio performance",
            },
            "sigma_select": {
                "name": "Sigma Select",
                "description": "Sales intelligence and lead scoring",
                "endpoints": "/api/v1/sigma-select",
                "quantum_advantage": "2.8x lead conversion",
            },
        },
        "features": [
            "Quantum-enhanced business operations",
            "Real-time monitoring and analytics",
            "Cross-business unit communication",
            "High Council administrative dashboard",
            "Automated decision making",
        ],
        "documentation": "/docs",
        "redoc": "/redoc",
    }


# Include routers
app.include_router(business_units_router, prefix="/api/v1", tags=["Business Units"])

app.include_router(
    high_council_router, prefix="/api/v1/high-council", tags=["High Council"]
)

app.include_router(monitoring_router, prefix="/api/v1/monitoring", tags=["Monitoring"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
