from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
import os

router = APIRouter()


class ConnectRequest(BaseModel):
    provider: str
    config: Dict[str, Any]


class IntegrationStatus(BaseModel):
    provider: str
    status: str
    connected_at: str
    last_sync: str


@router.post("/connect")
async def connect_provider(req: ConnectRequest):
    """Register/connect an external integration (UiPath/n8n/Mendix/Prismatic)"""
    provider = req.provider.lower()
    if provider not in ("uipath", "n8n", "mendix", "prismatic"):
        raise HTTPException(400, "Unsupported provider")

    # Store the config in DB (stub)
    # TODO: Implement actual database storage
    return {
        "status": "registered",
        "provider": provider,
        "message": f"Successfully connected {provider} integration",
    }


@router.get("/status")
async def get_integrations_status() -> List[IntegrationStatus]:
    """Get status of all connected integrations"""
    # Stub: return mock integration statuses
    return [
        IntegrationStatus(
            provider="uipath",
            status="connected",
            connected_at="2024-01-15T10:30:00Z",
            last_sync="2024-01-15T14:45:00Z",
        ),
        IntegrationStatus(
            provider="n8n",
            status="connected",
            connected_at="2024-01-14T09:15:00Z",
            last_sync="2024-01-15T13:20:00Z",
        ),
        IntegrationStatus(
            provider="mendix",
            status="pending",
            connected_at="2024-01-13T16:00:00Z",
            last_sync="2024-01-13T16:00:00Z",
        ),
        IntegrationStatus(
            provider="prismatic",
            status="disconnected",
            connected_at="2024-01-12T11:30:00Z",
            last_sync="2024-01-12T11:30:00Z",
        ),
    ]


@router.delete("/disconnect/{provider}")
async def disconnect_provider(provider: str):
    """Disconnect a specific integration provider"""
    provider = provider.lower()
    if provider not in ("uipath", "n8n", "mendix", "prismatic"):
        raise HTTPException(400, "Unsupported provider")

    # TODO: Implement actual disconnection logic
    return {
        "status": "disconnected",
        "provider": provider,
        "message": f"Successfully disconnected {provider} integration",
    }


@router.post("/test/{provider}")
async def test_integration(provider: str):
    """Test connection to a specific integration provider"""
    provider = provider.lower()
    if provider not in ("uipath", "n8n", "mendix", "prismatic"):
        raise HTTPException(400, "Unsupported provider")

    # TODO: Implement actual connection testing
    return {
        "status": "success",
        "provider": provider,
        "message": f"Successfully tested {provider} integration",
        "response_time_ms": 150,
    }
