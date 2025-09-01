from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import sigma_select, unified_dashboard, integrations, security

app = FastAPI(title="NQBA Phase2 - FLYFOX AI", version="0.2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sigma_select.router, prefix="/v2/sigma", tags=["SigmaSelect"])
app.include_router(unified_dashboard.router, prefix="/v2/dashboard", tags=["Dashboard"])
app.include_router(
    integrations.router, prefix="/v2/integrations", tags=["Integrations"]
)
app.include_router(security.router, prefix="/v2/security", tags=["Security"])


@app.get("/")
async def root():
    return {
        "service": "NQBA Phase2",
        "branding": "FLYFOX AI",
        "quantum_backend": "Dynex",
        "performance_multiplier": 410,
    }


@app.get("/health")
async def health():
    return {
        "ok": True,
        "service": "nqba-phase2-api",
        "quantum_backend": "dynex",
        "nvidia_accel": True,
        "multiplier": 410.0,
    }
