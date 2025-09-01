"""
Role-based access control for pricing API (FastAPI dependency).
"""

from fastapi import Depends, HTTPException, status, Request
import os

API_KEYS = os.environ.get("PRICING_API_KEYS", "demo-key").split(",")


async def require_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key."
        )
