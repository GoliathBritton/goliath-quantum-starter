from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models import Lead, LeadScoreRequest, LeadScore
from ..dynex_client import dynex_client
import uuid
import random

router = APIRouter()

# Sample leads data for demo
SAMPLE_LEADS = [
    {
        "id": "lead_001",
        "company_name": "TechCorp Solutions",
        "contact_name": "Sarah Johnson",
        "title": "CTO",
        "email": "sarah.johnson@techcorp.com",
        "phone": "+1-555-0123",
        "industry": "Technology",
        "company_size": 250,
        "annual_revenue": 15000000,
        "notes": "Interested in quantum optimization for supply chain"
    },
    {
        "id": "lead_002",
        "company_name": "Global Finance Inc",
        "contact_name": "Michael Chen",
        "title": "VP of Innovation",
        "email": "m.chen@globalfinance.com",
        "phone": "+1-555-0456",
        "industry": "Financial Services",
        "company_size": 1200,
        "annual_revenue": 85000000,
        "notes": "Exploring quantum algorithms for risk analysis"
    },
    {
        "id": "lead_003",
        "company_name": "MedTech Innovations",
        "contact_name": "Dr. Emily Rodriguez",
        "title": "Chief Science Officer",
        "email": "e.rodriguez@medtech.com",
        "phone": "+1-555-0789",
        "industry": "Healthcare",
        "company_size": 450,
        "annual_revenue": 32000000,
        "notes": "Quantum computing for drug discovery applications"
    }
]

@router.get("/", response_model=List[Lead])
async def get_leads(industry: Optional[str] = None, min_revenue: Optional[float] = None):
    """
    Get all leads with optional filtering by industry and minimum revenue.
    """
    leads = SAMPLE_LEADS.copy()
    
    if industry:
        leads = [lead for lead in leads if lead["industry"].lower() == industry.lower()]
    
    if min_revenue:
        leads = [lead for lead in leads if lead.get("annual_revenue", 0) >= min_revenue]
    
    return leads

@router.get("/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str):
    """
    Get a specific lead by ID.
    """
    lead = next((l for l in SAMPLE_LEADS if l["id"] == lead_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.post("/", response_model=Lead)
async def create_lead(lead: Lead):
    """
    Create a new lead.
    """
    if not lead.id:
        lead.id = f"lead_{uuid.uuid4().hex[:8]}"
    
    # Add to sample data (in production, this would go to a database)
    lead_dict = lead.dict()
    SAMPLE_LEADS.append(lead_dict)
    
    return lead_dict

@router.post("/score", response_model=List[LeadScore])
async def score_leads(request: LeadScoreRequest):
    """
    Score leads using quantum-enhanced algorithms.
    """
    scores = []
    
    for lead in request.leads:
        # Prepare payload for quantum scoring
        payload = {
            "company_name": lead.company_name,
            "industry": lead.industry or "unknown",
            "company_size": lead.company_size or 0,
            "annual_revenue": lead.annual_revenue or 0,
            "contact_title": lead.title or "unknown"
        }
        
        # Get quantum score
        result = dynex_client.solve_qubo(payload)
        
        # Generate priority based on score
        if result["score"] > 0.8:
            priority = "high"
        elif result["score"] > 0.6:
            priority = "medium"
        else:
            priority = "low"
        
        # Create detailed reasoning
        factors = result["factors"]
        reason = f"Market signal: {factors['market_signal_strength']:.2f}, Resource match: {factors['resource_match']:.2f}, Timing: {factors['timing_score']:.2f}"
        
        score = LeadScore(
            lead_id=lead.id,
            score=result["score"],
            reason=reason,
            dynamic_priority=priority
        )
        scores.append(score)
    
    return scores

@router.get("/analytics/conversion-forecast")
async def get_conversion_forecast():
    """
    Get quantum-enhanced conversion forecasting for current leads.
    """
    total_leads = len(SAMPLE_LEADS)
    
    # Simulate quantum-enhanced forecasting
    base_conversion_rate = 0.15  # 15% baseline
    quantum_enhancement = 2.3    # 2.3x improvement
    
    enhanced_rate = min(0.85, base_conversion_rate * quantum_enhancement)
    
    forecast = {
        "total_leads": total_leads,
        "baseline_conversion_rate": base_conversion_rate,
        "quantum_enhanced_rate": round(enhanced_rate, 3),
        "improvement_factor": quantum_enhancement,
        "projected_conversions": round(total_leads * enhanced_rate),
        "quantum_advantage": f"{round((quantum_enhancement - 1) * 100)}% improvement",
        "confidence_interval": [0.82, 0.94],
        "methodology": "Dynex QUBO optimization with market signal analysis"
    }
    
    return forecast

@router.get("/analytics/industry-breakdown")
async def get_industry_breakdown():
    """
    Get lead distribution and scoring by industry.
    """
    industry_stats = {}
    
    for lead in SAMPLE_LEADS:
        industry = lead.get("industry", "Unknown")
        if industry not in industry_stats:
            industry_stats[industry] = {
                "count": 0,
                "total_revenue": 0,
                "avg_company_size": 0,
                "quantum_score_avg": 0
            }
        
        industry_stats[industry]["count"] += 1
        industry_stats[industry]["total_revenue"] += lead.get("annual_revenue", 0)
        industry_stats[industry]["avg_company_size"] += lead.get("company_size", 0)
        
        # Simulate quantum scoring for analytics
        payload = {"industry": industry, "revenue": lead.get("annual_revenue", 0)}
        score = dynex_client.solve_qubo(payload)["score"]
        industry_stats[industry]["quantum_score_avg"] += score
    
    # Calculate averages
    for industry, stats in industry_stats.items():
        count = stats["count"]
        stats["avg_company_size"] = round(stats["avg_company_size"] / count)
        stats["quantum_score_avg"] = round(stats["quantum_score_avg"] / count, 3)
        stats["avg_revenue"] = round(stats["total_revenue"] / count)
    
    return {
        "industry_breakdown": industry_stats,
        "quantum_enhanced": True,
        "total_industries": len(industry_stats)
    }