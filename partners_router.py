"""Partner management router for NQBA Core API

Implements partner registration and management endpoints according to the OpenAPI specification.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
from datetime import datetime
import uuid
import secrets
from models import (
    PartnerRegistrationRequest,
    PartnerRegistrationResponse,
    Partner,
    TierUpdateRequest,
    PartnerTier,
    PartnerStatus,
    ErrorResponse
)
from auth_router import verify_token

# Create router
partners_router = APIRouter(prefix="/partners", tags=["partners"])

# Mock partner database (in production, use proper database)
MOCK_PARTNERS: Dict[str, Partner] = {}
PARTNER_API_KEYS: Dict[str, str] = {}  # api_key -> partner_id mapping


def generate_api_key() -> str:
    """Generate a secure API key for partners"""
    return f"pk_{secrets.token_urlsafe(32)}"


def get_partner_by_id(partner_id: str) -> Partner:
    """Get partner by ID or raise 404"""
    partner = MOCK_PARTNERS.get(partner_id)
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found"
        )
    return partner


@partners_router.post("/register", response_model=PartnerRegistrationResponse)
async def register_partner(registration: PartnerRegistrationRequest):
    """Register a new partner"""
    # Check if partner with this email already exists
    for partner in MOCK_PARTNERS.values():
        if partner.contact_email == registration.contact_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Partner with this email already exists"
            )
    
    # Generate partner ID and API key
    partner_id = f"partner_{uuid.uuid4().hex[:8]}"
    api_key = generate_api_key()
    
    # Create partner
    partner = Partner(
        id=partner_id,
        company_name=registration.company_name,
        contact_email=registration.contact_email,
        tier=registration.tier,
        status=PartnerStatus.pending,
        created_at=datetime.utcnow(),
        revenue_share=0.0
    )
    
    # Store partner and API key
    MOCK_PARTNERS[partner_id] = partner
    PARTNER_API_KEYS[api_key] = partner_id
    
    return PartnerRegistrationResponse(
        partner_id=partner_id,
        api_key=api_key,
        status=PartnerStatus.pending
    )


@partners_router.get("/{partner_id}", response_model=Partner)
async def get_partner(partner_id: str, current_user: dict = Depends(verify_token)):
    """Get partner details"""
    return get_partner_by_id(partner_id)


@partners_router.put("/{partner_id}/tier", response_model=Partner)
async def update_partner_tier(
    partner_id: str,
    tier_update: TierUpdateRequest,
    current_user: dict = Depends(verify_token)
):
    """Update partner tier"""
    partner = get_partner_by_id(partner_id)
    
    # Update tier
    partner.tier = tier_update.tier
    
    # Set revenue share based on tier
    revenue_shares = {
        PartnerTier.bronze: 0.05,
        PartnerTier.silver: 0.10,
        PartnerTier.gold: 0.15,
        PartnerTier.platinum: 0.20
    }
    partner.revenue_share = revenue_shares.get(tier_update.tier, 0.0)
    
    # Update in storage
    MOCK_PARTNERS[partner_id] = partner
    
    return partner


@partners_router.get("/", response_model=List[Partner])
async def list_partners(
    status: PartnerStatus = None,
    tier: PartnerTier = None,
    current_user: dict = Depends(verify_token)
):
    """List all partners with optional filtering"""
    partners = list(MOCK_PARTNERS.values())
    
    # Apply filters
    if status:
        partners = [p for p in partners if p.status == status]
    
    if tier:
        partners = [p for p in partners if p.tier == tier]
    
    return partners


@partners_router.post("/{partner_id}/approve")
async def approve_partner(partner_id: str, current_user: dict = Depends(verify_token)):
    """Approve a pending partner"""
    partner = get_partner_by_id(partner_id)
    
    if partner.status != PartnerStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Partner is not in pending status"
        )
    
    partner.status = PartnerStatus.active
    MOCK_PARTNERS[partner_id] = partner
    
    return {"message": "Partner approved successfully", "partner_id": partner_id}


@partners_router.post("/{partner_id}/suspend")
async def suspend_partner(partner_id: str, current_user: dict = Depends(verify_token)):
    """Suspend an active partner"""
    partner = get_partner_by_id(partner_id)
    
    if partner.status != PartnerStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Partner is not active"
        )
    
    partner.status = PartnerStatus.suspended
    MOCK_PARTNERS[partner_id] = partner
    
    return {"message": "Partner suspended successfully", "partner_id": partner_id}


@partners_router.post("/{partner_id}/terminate")
async def terminate_partner(partner_id: str, current_user: dict = Depends(verify_token)):
    """Terminate a partner"""
    partner = get_partner_by_id(partner_id)
    
    partner.status = PartnerStatus.terminated
    MOCK_PARTNERS[partner_id] = partner
    
    return {"message": "Partner terminated successfully", "partner_id": partner_id}


@partners_router.get("/{partner_id}/stats")
async def get_partner_stats(partner_id: str, current_user: dict = Depends(verify_token)):
    """Get partner statistics"""
    partner = get_partner_by_id(partner_id)
    
    # Mock statistics (in production, calculate from actual data)
    stats = {
        "partner_id": partner_id,
        "total_revenue": 12500.00,
        "monthly_revenue": 2500.00,
        "total_leads": 150,
        "converted_leads": 45,
        "conversion_rate": 0.30,
        "api_calls_this_month": 1250,
        "last_activity": datetime.utcnow().isoformat()
    }
    
    return stats


@partners_router.post("/{partner_id}/regenerate-api-key")
async def regenerate_api_key(partner_id: str, current_user: dict = Depends(verify_token)):
    """Regenerate API key for a partner"""
    partner = get_partner_by_id(partner_id)
    
    # Find and remove old API key
    old_api_key = None
    for api_key, pid in PARTNER_API_KEYS.items():
        if pid == partner_id:
            old_api_key = api_key
            break
    
    if old_api_key:
        del PARTNER_API_KEYS[old_api_key]
    
    # Generate new API key
    new_api_key = generate_api_key()
    PARTNER_API_KEYS[new_api_key] = partner_id
    
    return {
        "message": "API key regenerated successfully",
        "partner_id": partner_id,
        "new_api_key": new_api_key
    }