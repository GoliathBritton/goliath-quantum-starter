"""
Goliath of All Trade - Diversegy API Client
Integration with Diversegy energy brokerage platform
https://diversegy.com/ and https://partners.diversegypro.com/
"""

import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .models import (
    DiversegyCustomer, 
    DiversegyPlan, 
    DiversegyQuote, 
    DiversegyEnrollment,
    DiversegyPartnerStats,
    DiversegyAPIResponse
)

logger = logging.getLogger(__name__)

class DiversegyClient:
    """Goliath of All Trade client for Diversegy API integration"""
    
    def __init__(self, api_key: str, partner_id: str, base_url: str = "https://api.partners.diversegypro.com/v1"):
        self.api_key = api_key
        self.partner_id = partner_id
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Partner-ID": partner_id,
                "Content-Type": "application/json",
                "User-Agent": "Goliath-of-All-Trade/1.0"
            }
        )
    
    async def get_available_plans(self, state: str, energy_type: str) -> List[DiversegyPlan]:
        """Get available energy plans for a specific state and energy type"""
        try:
            response = await self.client.get(
                f"{self.base_url}/plans",
                params={"state": state, "energy_type": energy_type}
            )
            response.raise_for_status()
            return [DiversegyPlan(**plan) for plan in response.json().get("data", [])]
        except Exception as e:
            logger.error(f"Error fetching Diversegy plans: {str(e)}")
            raise
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> DiversegyCustomer:
        """Create a new customer in Diversegy platform"""
        try:
            response = await self.client.post(
                f"{self.base_url}/customers",
                json={**customer_data, "partner_id": self.partner_id}
            )
            response.raise_for_status()
            return DiversegyCustomer(**response.json().get("data", {}))
        except Exception as e:
            logger.error(f"Error creating Diversegy customer: {str(e)}")
            raise
    
    async def generate_quote(self, customer_id: str, plan_id: str, usage_data: Dict[str, Any]) -> DiversegyQuote:
        """Generate an energy quote for a customer"""
        try:
            response = await self.client.post(
                f"{self.base_url}/quotes",
                json={
                    "customer_id": customer_id,
                    "plan_id": plan_id,
                    "usage_data": usage_data,
                    "partner_id": self.partner_id
                }
            )
            response.raise_for_status()
            return DiversegyQuote(**response.json().get("data", {}))
        except Exception as e:
            logger.error(f"Error generating Diversegy quote: {str(e)}")
            raise
    
    async def create_enrollment(self, customer_id: str, plan_id: str, quote_id: Optional[str] = None) -> DiversegyEnrollment:
        """Enroll a customer in an energy plan"""
        try:
            enrollment_data = {
                "customer_id": customer_id,
                "plan_id": plan_id,
                "partner_id": self.partner_id
            }
            if quote_id:
                enrollment_data["quote_id"] = quote_id
                
            response = await self.client.post(
                f"{self.base_url}/enrollments",
                json=enrollment_data
            )
            response.raise_for_status()
            return DiversegyEnrollment(**response.json().get("data", {}))
        except Exception as e:
            logger.error(f"Error creating Diversegy enrollment: {str(e)}")
            raise
    
    async def get_partner_stats(self) -> DiversegyPartnerStats:
        """Get partner statistics from Diversegy"""
        try:
            response = await self.client.get(
                f"{self.base_url}/partners/{self.partner_id}/stats"
            )
            response.raise_for_status()
            return DiversegyPartnerStats(**response.json().get("data", {}))
        except Exception as e:
            logger.error(f"Error fetching Diversegy partner stats: {str(e)}")
            raise
            
    async def get_customer_enrollments(self, customer_id: str) -> List[DiversegyEnrollment]:
        """Get all enrollments for a specific customer"""
        try:
            response = await self.client.get(
                f"{self.base_url}/customers/{customer_id}/enrollments"
            )
            response.raise_for_status()
            return [DiversegyEnrollment(**enrollment) for enrollment in response.json().get("data", [])]
        except Exception as e:
            logger.error(f"Error fetching customer enrollments: {str(e)}")
            raise

# Initialize client with environment variables in production
# diversegy_client = DiversegyClient(
#     api_key=os.getenv("DIVERSEGY_API_KEY"),
#     partner_id=os.getenv("DIVERSEGY_PARTNER_ID"),
#     base_url=os.getenv("DIVERSEGY_API_URL", "https://api.partners.diversegypro.com/v1")
# )