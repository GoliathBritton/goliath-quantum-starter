from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import sigmaeq, leads, sales, revenue, analytics

app = FastAPI(title=settings.project_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "sigma-select-api",
        "quantum_backend": settings.quantum.preferred_backend,
        "nvidia_accel": settings.quantum.nvidia_accel,
        "multiplier": settings.quantum.performance_multiplier,
    }


app.include_router(sigmaeq.router, prefix=settings.api_prefix)
app.include_router(leads.router, prefix=settings.api_prefix)
app.include_router(sales.router, prefix=settings.api_prefix)
app.include_router(revenue.router, prefix=settings.api_prefix)
app.include_router(analytics.router, prefix=settings.api_prefix)
