from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Partner
from ..seed_data import PARTNERS

router = APIRouter(prefix="/api/partners", tags=["partners"])

@router.get("/", response_model=List[Partner])
async def list_partners():
    return PARTNERS

@router.get("/{partner_id}", response_model=Partner)
async def get_partner(partner_id: str):
    for p in PARTNERS:
        if p["id"] == partner_id:
            return p
    raise HTTPException(status_code=404, detail="Partner not found")

@router.get("/{partner_id}/metrics")
async def get_partner_metrics(partner_id: str):
    """Get partner performance metrics"""
    partner = next((p for p in PARTNERS if p["id"] == partner_id), None)
    
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    # Calculate metrics
    monthly_commission = partner["monthlyRevenue"] * partner["commissionRate"]
    revenue_per_customer = partner["monthlyRevenue"] / partner["totalCustomers"] if partner["totalCustomers"] > 0 else 0
    
    return {
        "partner_id": partner_id,
        "company": partner["company"],
        "monthly_commission": round(monthly_commission, 2),
        "revenue_per_customer": round(revenue_per_customer, 2),
        "tier": partner["tier"],
        "performance_score": round((partner["monthlyRevenue"] / 100000) * partner["commissionRate"] * 100, 1)
    }

@router.get("/analytics/summary")
async def get_partners_summary():
    """Get overall partner analytics summary"""
    total_revenue = sum(p["monthlyRevenue"] for p in PARTNERS)
    total_customers = sum(p["totalCustomers"] for p in PARTNERS)
    avg_commission_rate = sum(p["commissionRate"] for p in PARTNERS) / len(PARTNERS)
    
    tier_breakdown = {}
    for partner in PARTNERS:
        tier = partner["tier"]
        if tier not in tier_breakdown:
            tier_breakdown[tier] = {"count": 0, "revenue": 0}
        tier_breakdown[tier]["count"] += 1
        tier_breakdown[tier]["revenue"] += partner["monthlyRevenue"]
    
    return {
        "total_partners": len(PARTNERS),
        "total_monthly_revenue": total_revenue,
        "total_customers": total_customers,
        "average_commission_rate": round(avg_commission_rate, 3),
        "tier_breakdown": tier_breakdown,
        "top_performer": max(PARTNERS, key=lambda p: p["monthlyRevenue"])["company"]
    }