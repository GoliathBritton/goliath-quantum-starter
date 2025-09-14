from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes.partners import router as partners_router
from .routes.leads import router as leads_router
from .routes.oracle import router as oracle_router
from .routes.stripe import router as stripe_router
from .routes.auth import router as auth_router
import uvicorn

app = FastAPI(
    title="NQBA Quantum Sales API",
    description="Demo API for Quantum-Enhanced Sales Intelligence",
    version="1.0.0"
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
app.include_router(oracle_router, prefix="/api/quantum-nexus-engine", tags=["quantum-nexus-engine"])
app.include_router(stripe_router, prefix="/api", tags=["stripe"])

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