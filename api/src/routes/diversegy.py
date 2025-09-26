"""
Goliath of All Trade - Diversegy Integration Routes
API endpoints for Diversegy energy brokerage platform integration
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional
from ..diversegy.models import (
    DiversegyCustomer,
    DiversegyPlan,
    DiversegyQuote,
    DiversegyEnrollment,
    DiversegyPartnerStats,
    DiversegyAPIResponse,
    DiversegyEnergyType
)
from ..diversegy.client import DiversegyClient
import os
from datetime import datetime

# Initialize router with Goliath of All Trade branding
router = APIRouter(prefix="/diversegy", tags=["diversegy"])

# Initialize Diversegy client (in production, use environment variables)
# For demo purposes, using placeholder values
diversegy_client = DiversegyClient(
    api_key="demo_api_key",
    partner_id="goliath_partner_id",
    base_url="https://api.partners.diversegypro.com/v1"
)

@router.get("/plans", response_model=List[DiversegyPlan])
async def get_available_plans(state: str, energy_type: DiversegyEnergyType):
    """
    Get available energy plans for Goliath of All Trade customers
    """
    try:
        plans = await diversegy_client.get_available_plans(state, energy_type)
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")

@router.post("/customers", response_model=DiversegyCustomer)
async def create_customer(customer_data: Dict[str, Any] = Body(...)):
    """
    Create a new Goliath of All Trade customer in Diversegy platform
    """
    try:
        customer = await diversegy_client.create_customer(customer_data)
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")

@router.post("/quotes", response_model=DiversegyQuote)
async def generate_quote(
    customer_id: str,
    plan_id: str,
    usage_data: Dict[str, Any] = Body(...)
):
    """
    Generate an energy quote for a Goliath of All Trade customer
    """
    try:
        quote = await diversegy_client.generate_quote(customer_id, plan_id, usage_data)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quote: {str(e)}")

@router.post("/enrollments", response_model=DiversegyEnrollment)
async def create_enrollment(
    customer_id: str,
    plan_id: str,
    quote_id: Optional[str] = None
):
    """
    Enroll a Goliath of All Trade customer in an energy plan
    """
    try:
        enrollment = await diversegy_client.create_enrollment(customer_id, plan_id, quote_id)
        return enrollment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating enrollment: {str(e)}")

@router.get("/partner/stats", response_model=DiversegyPartnerStats)
async def get_partner_stats():
    """
    Get Goliath of All Trade partner statistics from Diversegy
    """
    try:
        stats = await diversegy_client.get_partner_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching partner stats: {str(e)}")

@router.get("/customers/{customer_id}/enrollments", response_model=List[DiversegyEnrollment])
async def get_customer_enrollments(customer_id: str):
    """
    Get all enrollments for a specific Goliath of All Trade customer
    """
    try:
        enrollments = await diversegy_client.get_customer_enrollments(customer_id)
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching customer enrollments: {str(e)}")