from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes.partners import router as partners_router
from .routes.leads import router as leads_router
from .routes.qnexus import router as qnexus_router
from .routes.auth import router as auth_router
from .routes.entitlements import router as entitlements_router
from .routes.security import router as security_router
from .routes.performance import router as performance_router
from .security.middleware import SecurityMiddleware
import uvicorn

app = FastAPI(
    title="NQBA Quantum Sales API",
    description="Demo API for Quantum-Enhanced Sales Intelligence",
    version="1.0.0"
)

# Security middleware (should be added first)
app.add_middleware(
    SecurityMiddleware,
    enable_rate_limiting=True,
    enable_audit_logging=True,
    enable_ip_filtering=True,
    enable_compliance_checks=True
)

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
app.include_router(qnexus_router, prefix="/api/quantum-nexus-engine", tags=["quantum-nexus-engine"])
app.include_router(stripe_router, prefix="/api", tags=["stripe"])
app.include_router(entitlements_router, prefix="/api", tags=["entitlements"])
app.include_router(security_router, prefix="/api/security", tags=["security"])
app.include_router(performance_router, prefix="/api/performance", tags=["performance"])

@app.get("/")
async def root():
    return {
        "message": "NQBA Quantum Sales API",
        "version": "1.0.0",
        "status": "operational",
        "quantum_enhanced": True
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "quantum_core": "operational",
        "dynex_simulation": "active"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)