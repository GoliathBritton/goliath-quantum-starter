"""
NQBA Monitoring API Router

Provides REST API endpoints for system monitoring and metrics.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def monitoring_info():
    """Get monitoring information"""
    return {
        "message": "NQBA Monitoring API",
        "description": "System monitoring and metrics endpoints",
        "status": "coming_soon",
    }
