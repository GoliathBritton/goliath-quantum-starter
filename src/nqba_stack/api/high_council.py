"""
NQBA High Council API Router

Provides REST API endpoints for the High Council administrative dashboard.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def high_council_info():
    """Get High Council information"""
    return {
        "message": "NQBA High Council API",
        "description": "Administrative oversight and management endpoints",
        "status": "coming_soon",
    }
