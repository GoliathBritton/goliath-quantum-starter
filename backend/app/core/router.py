from fastapi import APIRouter
from app.api.v1_agents import router as agents_router
from app.api.v1_chat import router as chat_router
from app.api.v1_voice import router as voice_router
from app.api.v1_subs import router as subs_router
from app.api.v1_crm import router as crm_router

# Main API router
api_router = APIRouter()

# Include all v1 API routes
api_router.include_router(agents_router, prefix="/v1/agents", tags=["agents"])
api_router.include_router(chat_router, prefix="/v1/chat", tags=["chat"])
api_router.include_router(voice_router, prefix="/v1/voice", tags=["voice"])
api_router.include_router(subs_router, prefix="/v1/subs", tags=["subscriptions"])
api_router.include_router(crm_router, prefix="/v1/crm", tags=["goliathcrm"])

# Health check for API
@api_router.get("/health")
def api_health():
    """API health check"""
    return {
        "status": "healthy",
        "version": "v1",
        "endpoints": [
            "/v1/agents",
            "/v1/chat", 
            "/v1/voice",
            "/v1/subs",
            "/v1/crm"
        ]
    }
