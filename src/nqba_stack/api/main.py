#!/usr/bin/env python3
"""
🚀 NQBA Stack - Main FastAPI Application

Main FastAPI application for the NQBA ecosystem with business unit
integration, authentication, and comprehensive API endpoints.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .business_units import router as business_units_router
from .high_council import router as high_council_router
from .monitoring import router as monitoring_router
from .auth import router as auth_router
from ..business_integration import business_unit_manager
from ..business_integration.flyfox_ai import FLYFOXAIBusinessUnit
from ..core.settings import get_settings
from ..core.ltc_automation import LTCLogger

# Initialize logger
logger = LTCLogger("nqba_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting NQBA Stack API...")

    try:
        # Initialize business unit manager
        await business_unit_manager.initialize()
        logger.info("✅ Business unit manager initialized")

        # Register FLYFOX AI business unit
        flyfox_ai_unit = FLYFOXAIBusinessUnit()
        await business_unit_manager.register_business_unit(flyfox_ai_unit)
        logger.info("✅ FLYFOX AI business unit registered")

        # Initialize authentication system
        from ..auth import AuthManager

        _ = AuthManager()  # Initialize AuthManager
        logger.info("✅ Authentication system initialized")

        logger.info("🚀 NQBA Stack API startup complete!")

    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("🔄 Shutting down NQBA Stack API...")

    try:
        # Shutdown business unit manager
        await business_unit_manager.shutdown()
        logger.info("✅ Business unit manager shutdown complete")

        logger.info("✅ NQBA Stack API shutdown complete!")

    except Exception as e:
        logger.error(f"❌ Shutdown error: {str(e)}")


# Create FastAPI app
app = FastAPI(
    title="NQBA Stack API",
    description="Neuromorphic Quantum Business Architecture - The Operating System of the Intelligence Economy",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Get settings
settings = get_settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()

    # Log request
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )

    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422, content={"error": "Validation error", "details": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"General Exception: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "detail": str(exc)}
    )


# Core endpoints
@app.get("/", tags=["Core"])
async def root():
    """Root endpoint with NQBA ecosystem information"""
    return {
        "message": "🚀 Welcome to NQBA Stack - The Operating System of the Intelligence Economy",
        "version": "2.0.0",
        "ecosystem": "Neuromorphic Quantum Business Architecture",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "info": "/info",
    }


@app.get("/health", tags=["Core"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check business unit manager health
        ecosystem_status = await business_unit_manager.get_ecosystem_status()

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "ecosystem": ecosystem_status,
            "version": "2.0.0",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/info", tags=["Core"])
async def system_info():
    """System information endpoint"""
    settings = get_settings()

    return {
        "system": "NQBA Stack",
        "version": "2.0.0",
        "description": "Neuromorphic Quantum Business Architecture",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "cors_origins": settings.ALLOWED_ORIGINS,
        "api_docs": "/docs",
        "redoc": "/redoc",
    }


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(business_units_router, prefix="/api/v1")
app.include_router(high_council_router, prefix="/api/v1")
app.include_router(monitoring_router, prefix="/api/v1")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Additional startup tasks"""
    logger.info("🚀 NQBA Stack API startup event triggered")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Additional shutdown tasks"""
    logger.info("🔄 NQBA Stack API shutdown event triggered")
