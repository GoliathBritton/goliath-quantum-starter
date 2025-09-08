"""Sigma scoring router for NQBA Core API

Implements SigmaEQ scoring endpoints according to the OpenAPI specification.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import random
from models import (
    Lead,
    ScoreResponse,
    ScoreFactor,
    ScoreImpact,
    ErrorResponse
)
from auth_router import verify_token

# Create router
sigma_router = APIRouter(prefix="/sigma", tags=["sigma"])

# Mock scoring models
SCORING_MODELS = [
    {
        "id": "sigmaeq_v1",
        "name": "SigmaEQ Lead Scoring v1.0",
        "description": "Advanced quantum-enhanced lead scoring model",
        "version": "1.0.0",
        "accuracy": 0.87,
        "features": ["email_domain", "company_size", "industry", "engagement_score"],
        "created_at": "2024-01-01T00:00:00Z",
        "is_active": True
    },
    {
        "id": "sigmaeq_v2",
        "name": "SigmaEQ Lead Scoring v2.0",
        "description": "Enhanced model with neuromorphic processing",
        "version": "2.0.0",
        "accuracy": 0.92,
        "features": ["email_domain", "company_size", "industry", "engagement_score", "social_signals", "behavioral_patterns"],
        "created_at": "2024-06-01T00:00:00Z",
        "is_active": True
    },
    {
        "id": "sigmaeq_quantum",
        "name": "SigmaEQ Quantum Scoring",
        "description": "Quantum-powered scoring with superposition analysis",
        "version": "3.0.0-beta",
        "accuracy": 0.95,
        "features": ["quantum_entanglement", "superposition_analysis", "quantum_interference", "all_classical_features"],
        "created_at": "2024-12-01T00:00:00Z",
        "is_active": False  # Beta model
    }
]


def calculate_advanced_score(lead: Lead, model_id: str = "sigmaeq_v2") -> ScoreResponse:
    """Calculate an advanced score using SigmaEQ algorithms"""
    model = next((m for m in SCORING_MODELS if m["id"] == model_id), SCORING_MODELS[1])
    
    # Base score with quantum enhancement
    base_score = 45.0 + random.uniform(-5, 5)  # Add some randomness for realism
    factors = []
    
    # Email domain analysis
    if lead.email and '@' in lead.email:
        domain = lead.email.split('@')[1].lower()
        
        # Corporate domains get higher scores
        corporate_domains = ['microsoft.com', 'google.com', 'apple.com', 'amazon.com', 'salesforce.com']
        enterprise_domains = ['.gov', '.edu', '.org']
        
        if any(domain.endswith(ed) for ed in enterprise_domains):
            domain_score = 25
            impact = ScoreImpact.positive
        elif domain in corporate_domains:
            domain_score = 20
            impact = ScoreImpact.positive
        elif domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
            domain_score = -8
            impact = ScoreImpact.negative
        else:
            domain_score = 12
            impact = ScoreImpact.positive
        
        base_score += domain_score
        factors.append(ScoreFactor(
            name="Email Domain Authority",
            weight=0.25,
            value=abs(domain_score),
            impact=impact
        ))
    
    # Company analysis
    if lead.company:
        company_name = lead.company.lower()
        
        # Fortune 500 indicators
        fortune_indicators = ['inc', 'corp', 'corporation', 'ltd', 'llc', 'technologies', 'systems']
        if any(indicator in company_name for indicator in fortune_indicators):
            company_score = 18
            impact = ScoreImpact.positive
        else:
            company_score = 8
            impact = ScoreImpact.positive
        
        base_score += company_score
        factors.append(ScoreFactor(
            name="Company Profile",
            weight=0.30,
            value=company_score,
            impact=impact
        ))
    
    # Contact completeness
    completeness_score = 0
    if lead.name:
        completeness_score += 5
    if lead.phone:
        completeness_score += 8
    if lead.company:
        completeness_score += 7
    
    if completeness_score > 0:
        base_score += completeness_score
        factors.append(ScoreFactor(
            name="Contact Completeness",
            weight=0.15,
            value=completeness_score,
            impact=ScoreImpact.positive
        ))
    
    # Industry analysis (from custom fields)
    if lead.custom_fields and 'industry' in lead.custom_fields:
        industry = lead.custom_fields['industry'].lower()
        high_value_industries = ['technology', 'finance', 'healthcare', 'manufacturing', 'consulting']
        
        if industry in high_value_industries:
            industry_score = 15
            impact = ScoreImpact.positive
        else:
            industry_score = 5
            impact = ScoreImpact.neutral
        
        base_score += industry_score
        factors.append(ScoreFactor(
            name="Industry Vertical",
            weight=0.20,
            value=industry_score,
            impact=impact
        ))
    
    # Quantum enhancement factor (for quantum model)
    if model_id == "sigmaeq_quantum":
        quantum_boost = random.uniform(5, 15)
        base_score += quantum_boost
        factors.append(ScoreFactor(
            name="Quantum Superposition Analysis",
            weight=0.35,
            value=quantum_boost,
            impact=ScoreImpact.positive
        ))
    
    # Engagement prediction (mock)
    engagement_score = random.uniform(3, 12)
    base_score += engagement_score
    factors.append(ScoreFactor(
        name="Predicted Engagement",
        weight=0.10,
        value=engagement_score,
        impact=ScoreImpact.positive
    ))
    
    # Ensure score is within bounds
    final_score = max(0, min(100, base_score))
    
    # Calculate confidence based on model accuracy and data completeness
    data_completeness = len([f for f in [lead.name, lead.company, lead.phone] if f]) / 3
    confidence = min(0.98, model["accuracy"] * data_completeness + 0.1)
    
    return ScoreResponse(
        lead_id=lead.id or f"temp_{uuid.uuid4().hex[:8]}",
        score=round(final_score, 2),
        confidence=round(confidence, 3),
        factors=factors,
        model_version=model["version"],
        scored_at=datetime.utcnow()
    )


@sigma_router.post("/score", response_model=ScoreResponse)
async def score_lead(
    lead: Lead,
    model_id: str = "sigmaeq_v2",
    current_user: dict = Depends(verify_token)
):
    """Score a lead using SigmaEQ algorithms"""
    # Validate model exists
    model = next((m for m in SCORING_MODELS if m["id"] == model_id), None)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scoring model '{model_id}' not found"
        )
    
    if not model["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scoring model '{model_id}' is not active"
        )
    
    # Validate lead data
    if not lead.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required for scoring"
        )
    
    return calculate_advanced_score(lead, model_id)


@sigma_router.get("/models")
async def list_scoring_models(current_user: dict = Depends(verify_token)):
    """List available scoring models"""
    return SCORING_MODELS


@sigma_router.get("/models/{model_id}")
async def get_scoring_model(model_id: str, current_user: dict = Depends(verify_token)):
    """Get details of a specific scoring model"""
    model = next((m for m in SCORING_MODELS if m["id"] == model_id), None)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scoring model not found"
        )
    
    return model


@sigma_router.post("/batch-score")
async def batch_score_leads(
    leads: List[Lead],
    model_id: str = "sigmaeq_v2",
    current_user: dict = Depends(verify_token)
):
    """Score multiple leads in batch"""
    # Validate model exists
    model = next((m for m in SCORING_MODELS if m["id"] == model_id), None)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scoring model '{model_id}' not found"
        )
    
    if not model["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scoring model '{model_id}' is not active"
        )
    
    # Limit batch size
    if len(leads) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch size cannot exceed 100 leads"
        )
    
    results = []
    errors = []
    
    for i, lead in enumerate(leads):
        try:
            if not lead.email:
                errors.append({
                    "index": i,
                    "error": "Email is required for scoring"
                })
                continue
            
            score_result = calculate_advanced_score(lead, model_id)
            results.append({
                "index": i,
                "score_result": score_result
            })
        
        except Exception as e:
            errors.append({
                "index": i,
                "error": str(e)
            })
    
    return {
        "model_id": model_id,
        "model_version": model["version"],
        "total_leads": len(leads),
        "successful_scores": len(results),
        "errors": len(errors),
        "results": results,
        "errors_detail": errors,
        "scored_at": datetime.utcnow()
    }


@sigma_router.get("/analytics/model-performance")
async def get_model_performance(current_user: dict = Depends(verify_token)):
    """Get performance analytics for scoring models"""
    # Mock performance data
    performance_data = []
    
    for model in SCORING_MODELS:
        if model["is_active"]:
            performance_data.append({
                "model_id": model["id"],
                "model_name": model["name"],
                "version": model["version"],
                "accuracy": model["accuracy"],
                "total_scores": random.randint(1000, 10000),
                "avg_score": round(random.uniform(45, 75), 2),
                "high_confidence_scores": random.randint(70, 95),
                "last_30_days_usage": random.randint(100, 1000),
                "conversion_rate": round(random.uniform(0.15, 0.35), 3)
            })
    
    return {
        "models": performance_data,
        "generated_at": datetime.utcnow()
    }


@sigma_router.get("/analytics/score-distribution")
async def get_score_distribution(
    model_id: str = "sigmaeq_v2",
    days: int = 30,
    current_user: dict = Depends(verify_token)
):
    """Get score distribution analytics"""
    # Mock distribution data
    distribution = {
        "model_id": model_id,
        "period_days": days,
        "total_scores": random.randint(500, 2000),
        "score_ranges": {
            "0-20": random.randint(50, 150),
            "21-40": random.randint(100, 300),
            "41-60": random.randint(200, 500),
            "61-80": random.randint(150, 400),
            "81-100": random.randint(50, 200)
        },
        "average_score": round(random.uniform(45, 70), 2),
        "median_score": round(random.uniform(50, 65), 2),
        "confidence_distribution": {
            "high (>0.8)": random.randint(60, 85),
            "medium (0.5-0.8)": random.randint(10, 25),
            "low (<0.5)": random.randint(2, 10)
        },
        "generated_at": datetime.utcnow()
    }
    
    return distribution