#!/usr/bin/env python3
"""
NQBA QUBO Quantum Lead Scoring Service
Integrates with NQBA engine for quantum-optimized lead scoring and prioritization
"""

import asyncio
import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import redis
import pickle

# Import NQBA components
try:
    from ..nqba.engine import NQBAEngine
    from ..goliath.quantum.qubo_solver import QUBOSolver
except ImportError:
    # Fallback for development
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.nqba.engine import NQBAEngine
    from src.goliath.quantum.qubo_solver import QUBOSolver

from .lead_ingestion_engine import Lead, LeadIngestionEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API
class LeadScoreRequest(BaseModel):
    lead_ids: List[str]
    scoring_criteria: Optional[Dict] = None
    priority_weights: Optional[Dict] = None

class LeadScoreResponse(BaseModel):
    lead_id: str
    quantum_score: float
    priority_tier: str
    confidence: float
    scoring_factors: Dict
    recommendations: List[str]

class BatchScoreResponse(BaseModel):
    total_leads: int
    processed: int
    failed: int
    results: List[LeadScoreResponse]
    processing_time: float

@dataclass
class ScoringCriteria:
    """Quantum scoring criteria configuration"""
    industry_weights: Dict[str, float]
    title_weights: Dict[str, float]
    company_size_weights: Dict[str, float]
    revenue_weights: Dict[str, float]
    engagement_weights: Dict[str, float]
    temporal_decay: float = 0.95  # Daily decay factor
    quantum_optimization: bool = True

class QuantumLeadScorer:
    """Main quantum lead scoring engine using NQBA and QUBO"""
    
    def __init__(self, 
                 db_url: str = "postgresql://localhost/quantum_leads",
                 redis_url: str = "redis://localhost:6379"):
        
        # Database setup
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Redis for caching
        self.redis_client = redis.from_url(redis_url)
        
        # Initialize NQBA and QUBO components
        self.nqba_engine = NQBAEngine()
        self.qubo_solver = QUBOSolver()
        
        # Default scoring criteria
        self.default_criteria = ScoringCriteria(
            industry_weights={
                'Technology': 0.9,
                'Financial Services': 0.85,
                'Healthcare': 0.8,
                'Manufacturing': 0.75,
                'Retail': 0.7,
                'Education': 0.65,
                'Government': 0.6,
                'Other': 0.5
            },
            title_weights={
                'CEO': 0.95, 'CTO': 0.9, 'CFO': 0.9, 'COO': 0.85,
                'VP': 0.8, 'Director': 0.75, 'Manager': 0.7,
                'Senior': 0.65, 'Lead': 0.6, 'Analyst': 0.55,
                'Coordinator': 0.5, 'Assistant': 0.4, 'Other': 0.3
            },
            company_size_weights={
                '1000+': 0.9, '500-999': 0.85, '100-499': 0.8,
                '50-99': 0.7, '10-49': 0.6, '1-9': 0.4, 'Unknown': 0.3
            },
            revenue_weights={
                '$100M+': 0.95, '$50M-$100M': 0.9, '$10M-$50M': 0.85,
                '$1M-$10M': 0.75, '$100K-$1M': 0.6, '<$100K': 0.4, 'Unknown': 0.3
            },
            engagement_weights={
                'website_visit': 0.3, 'email_open': 0.2, 'email_click': 0.4,
                'content_download': 0.6, 'demo_request': 0.9, 'pricing_page': 0.8,
                'linkedin_connect': 0.5, 'referral': 0.7
            }
        )
        
        # Performance tracking
        self.scoring_stats = {
            'total_scored': 0,
            'quantum_optimized': 0,
            'cache_hits': 0,
            'avg_processing_time': 0.0
        }
    
    def extract_lead_features(self, lead: Lead) -> Dict[str, float]:
        """Extract numerical features from lead data for quantum processing"""
        features = {}
        
        # Industry scoring
        industry = lead.industry or 'Other'
        features['industry_score'] = self.default_criteria.industry_weights.get(industry, 0.5)
        
        # Title scoring
        title = lead.title or 'Other'
        title_score = 0.3  # Default
        for key, weight in self.default_criteria.title_weights.items():
            if key.lower() in title.lower():
                title_score = max(title_score, weight)
        features['title_score'] = title_score
        
        # Company size scoring
        employees = lead.employees or 'Unknown'
        features['company_size_score'] = self.default_criteria.company_size_weights.get(employees, 0.3)
        
        # Revenue scoring
        revenue = lead.revenue or 'Unknown'
        features['revenue_score'] = self.default_criteria.revenue_weights.get(revenue, 0.3)
        
        # Data completeness score
        completeness_factors = [
            1.0 if lead.email_valid else 0.0,
            1.0 if lead.phone_valid else 0.0,
            1.0 if lead.company else 0.0,
            1.0 if lead.title else 0.0,
            1.0 if lead.industry else 0.0,
            1.0 if lead.linkedin_url else 0.0,
            1.0 if lead.website else 0.0
        ]
        features['completeness_score'] = sum(completeness_factors) / len(completeness_factors)
        
        # Temporal freshness (newer leads score higher)
        if lead.created_at:
            days_old = (datetime.utcnow() - lead.created_at).days
            features['freshness_score'] = self.default_criteria.temporal_decay ** days_old
        else:
            features['freshness_score'] = 0.5
        
        # Contact attempt penalty
        attempt_penalty = max(0.1, 1.0 - (lead.contact_attempts * 0.1))
        features['attempt_score'] = attempt_penalty
        
        return features
    
    def build_qubo_matrix(self, leads_features: List[Dict[str, float]]) -> np.ndarray:
        """Build QUBO matrix for quantum optimization of lead prioritization"""
        n_leads = len(leads_features)
        
        # Initialize QUBO matrix
        Q = np.zeros((n_leads, n_leads))
        
        # Diagonal terms (individual lead scores)
        for i, features in enumerate(leads_features):
            # Weighted combination of features
            individual_score = (
                features['industry_score'] * 0.25 +
                features['title_score'] * 0.25 +
                features['company_size_score'] * 0.15 +
                features['revenue_score'] * 0.15 +
                features['completeness_score'] * 0.1 +
                features['freshness_score'] * 0.05 +
                features['attempt_score'] * 0.05
            )
            Q[i, i] = -individual_score  # Negative for maximization
        
        # Off-diagonal terms (lead interactions/conflicts)
        for i in range(n_leads):
            for j in range(i + 1, n_leads):
                # Penalize selecting leads from same company (diversification)
                if (leads_features[i].get('company') == leads_features[j].get('company') and 
                    leads_features[i].get('company') is not None):
                    Q[i, j] = 0.1  # Small penalty for same company
                
                # Bonus for complementary industries
                industry_i = leads_features[i].get('industry_score', 0)
                industry_j = leads_features[j].get('industry_score', 0)
                if abs(industry_i - industry_j) > 0.3:  # Different industries
                    Q[i, j] -= 0.05  # Small bonus for diversity
        
        return Q
    
    async def quantum_score_leads(self, leads: List[Lead], max_selection: int = None) -> List[Tuple[Lead, float, Dict]]:
        """Use quantum optimization to score and prioritize leads"""
        if not leads:
            return []
        
        start_time = datetime.utcnow()
        
        # Extract features for all leads
        leads_features = []
        for lead in leads:
            features = self.extract_lead_features(lead)
            features['lead_id'] = str(lead.id)
            features['company'] = lead.company
            leads_features.append(features)
        
        # Build QUBO matrix
        Q = self.build_qubo_matrix(leads_features)
        
        # Solve using quantum optimization
        if len(leads) > 1 and self.default_criteria.quantum_optimization:
            try:
                # Use NQBA for quantum optimization
                solution = await self.nqba_engine.solve_qubo(Q, max_selection or len(leads) // 2)
                quantum_optimized = True
                self.scoring_stats['quantum_optimized'] += 1
            except Exception as e:
                logger.warning(f"Quantum optimization failed, falling back to classical: {e}")
                # Fallback to classical scoring
                solution = np.diag(Q).argsort()[:max_selection or len(leads)]
                quantum_optimized = False
        else:
            # Classical scoring for single leads or when quantum is disabled
            solution = np.diag(Q).argsort()[:max_selection or len(leads)]
            quantum_optimized = False
        
        # Generate results
        results = []
        for i, lead in enumerate(leads):
            features = leads_features[i]
            
            # Calculate final score
            base_score = -Q[i, i]  # Convert back from negative
            
            # Apply quantum optimization bonus if selected
            if quantum_optimized and i in solution:
                quantum_bonus = 0.1
            else:
                quantum_bonus = 0.0
            
            final_score = min(1.0, base_score + quantum_bonus)
            
            # Determine priority tier
            if final_score >= 0.8:
                priority_tier = 'hot'
            elif final_score >= 0.6:
                priority_tier = 'warm'
            elif final_score >= 0.4:
                priority_tier = 'cold'
            else:
                priority_tier = 'ice'
            
            # Generate recommendations
            recommendations = self.generate_recommendations(lead, features, final_score)
            
            results.append((lead, final_score, {
                'features': features,
                'priority_tier': priority_tier,
                'quantum_optimized': quantum_optimized,
                'recommendations': recommendations,
                'confidence': min(1.0, features['completeness_score'] + 0.2)
            }))
        
        # Update stats
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        self.scoring_stats['total_scored'] += len(leads)
        self.scoring_stats['avg_processing_time'] = (
            (self.scoring_stats['avg_processing_time'] * (self.scoring_stats['total_scored'] - len(leads)) + 
             processing_time) / self.scoring_stats['total_scored']
        )
        
        return results
    
    def generate_recommendations(self, lead: Lead, features: Dict, score: float) -> List[str]:
        """Generate actionable recommendations for lead engagement"""
        recommendations = []
        
        # Score-based recommendations
        if score >= 0.8:
            recommendations.append("🔥 Priority contact - call within 24 hours")
            recommendations.append("📞 Use senior sales rep for initial contact")
        elif score >= 0.6:
            recommendations.append("📧 Send personalized email sequence")
            recommendations.append("🔗 Connect on LinkedIn first")
        elif score >= 0.4:
            recommendations.append("📰 Add to nurture campaign")
            recommendations.append("📊 Monitor for engagement signals")
        else:
            recommendations.append("❄️ Low priority - quarterly check-in")
        
        # Feature-based recommendations
        if features['completeness_score'] < 0.6:
            recommendations.append("🔍 Enrich lead data before contact")
        
        if features['title_score'] >= 0.8:
            recommendations.append("👑 Executive-level outreach approach")
        
        if features['company_size_score'] >= 0.8:
            recommendations.append("🏢 Enterprise sales process")
        
        if lead.contact_attempts > 3:
            recommendations.append("⏸️ Consider cooling-off period")
        
        if not lead.phone_valid and lead.email_valid:
            recommendations.append("📧 Email-first approach (no valid phone)")
        
        return recommendations
    
    async def score_lead_batch(self, lead_ids: List[str]) -> List[LeadScoreResponse]:
        """Score a batch of leads by ID"""
        session = self.SessionLocal()
        
        try:
            # Fetch leads from database
            leads = session.query(Lead).filter(Lead.id.in_(lead_ids)).all()
            
            if not leads:
                return []
            
            # Check cache first
            cached_results = []
            uncached_leads = []
            
            for lead in leads:
                cache_key = f"lead_score:{lead.id}:{lead.updated_at.timestamp()}"
                cached_score = self.redis_client.get(cache_key)
                
                if cached_score:
                    cached_results.append(pickle.loads(cached_score))
                    self.scoring_stats['cache_hits'] += 1
                else:
                    uncached_leads.append(lead)
            
            # Score uncached leads
            new_results = []
            if uncached_leads:
                scoring_results = await self.quantum_score_leads(uncached_leads)
                
                for lead, score, metadata in scoring_results:
                    result = LeadScoreResponse(
                        lead_id=str(lead.id),
                        quantum_score=score,
                        priority_tier=metadata['priority_tier'],
                        confidence=metadata['confidence'],
                        scoring_factors=metadata['features'],
                        recommendations=metadata['recommendations']
                    )
                    
                    # Cache result
                    cache_key = f"lead_score:{lead.id}:{lead.updated_at.timestamp()}"
                    self.redis_client.setex(cache_key, 3600, pickle.dumps(result))  # 1 hour cache
                    
                    # Update database
                    session.execute(
                        update(Lead)
                        .where(Lead.id == lead.id)
                        .values(
                            quantum_score=score,
                            priority_tier=metadata['priority_tier'],
                            updated_at=datetime.utcnow()
                        )
                    )
                    
                    new_results.append(result)
                
                session.commit()
            
            return cached_results + new_results
        
        finally:
            session.close()
    
    def get_scoring_stats(self) -> Dict:
        """Get performance statistics"""
        return self.scoring_stats.copy()

# FastAPI application
app = FastAPI(
    title="Quantum Lead Scoring API",
    description="NQBA-powered quantum lead scoring and prioritization",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scorer instance
scorer = None

@app.on_event("startup")
async def startup_event():
    global scorer
    scorer = QuantumLeadScorer()
    logger.info("Quantum Lead Scoring API started")

@app.post("/score/batch", response_model=BatchScoreResponse)
async def score_lead_batch(request: LeadScoreRequest, background_tasks: BackgroundTasks):
    """Score a batch of leads using quantum optimization"""
    start_time = datetime.utcnow()
    
    try:
        results = await scorer.score_lead_batch(request.lead_ids)
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return BatchScoreResponse(
            total_leads=len(request.lead_ids),
            processed=len(results),
            failed=len(request.lead_ids) - len(results),
            results=results,
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Error scoring leads: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/score/stats")
async def get_scoring_stats():
    """Get scoring performance statistics"""
    return scorer.get_scoring_stats()

@app.post("/score/auto-batch")
async def auto_score_new_leads(background_tasks: BackgroundTasks):
    """Automatically score all new leads"""
    session = scorer.SessionLocal()
    
    try:
        # Get all unscored leads
        unscored_leads = session.query(Lead).filter(
            Lead.quantum_score == 0.0,
            Lead.email_valid == True
        ).limit(1000).all()  # Process in batches of 1000
        
        if not unscored_leads:
            return {"message": "No new leads to score", "processed": 0}
        
        lead_ids = [str(lead.id) for lead in unscored_leads]
        
        # Score in background
        background_tasks.add_task(scorer.score_lead_batch, lead_ids)
        
        return {
            "message": f"Started scoring {len(lead_ids)} leads",
            "processed": len(lead_ids)
        }
    
    finally:
        session.close()

@app.get("/leads/top/{limit}")
async def get_top_leads(limit: int = 100):
    """Get top-scored leads for immediate action"""
    session = scorer.SessionLocal()
    
    try:
        top_leads = session.query(Lead).filter(
            Lead.quantum_score > 0.0
        ).order_by(Lead.quantum_score.desc()).limit(limit).all()
        
        results = []
        for lead in top_leads:
            results.append({
                "id": str(lead.id),
                "name": f"{lead.first_name} {lead.last_name}",
                "email": lead.email,
                "company": lead.company,
                "title": lead.title,
                "quantum_score": lead.quantum_score,
                "priority_tier": lead.priority_tier,
                "contact_attempts": lead.contact_attempts,
                "created_at": lead.created_at.isoformat() if lead.created_at else None
            })
        
        return {"leads": results, "total": len(results)}
    
    finally:
        session.close()

if __name__ == "__main__":
    uvicorn.run(
        "quantum_lead_scoring:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )