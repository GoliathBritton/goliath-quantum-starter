from celery import Celery
from typing import Dict, Any, List, Optional
import json
import uuid
import time
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog
import asyncio
from ..dynex_client import DynexClient

logger = structlog.get_logger()

# Get Celery app instance
from ..app_consolidated import celery_app

@celery_app.task(bind=True, name="leads.score_lead")
def score_lead_async(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Asynchronously score a lead using quantum-enhanced algorithms
    
    Args:
        lead_data: Lead information for scoring
        
    Returns:
        Lead scoring results
    """
    task_id = self.request.id
    logger.info("Starting lead scoring", task_id=task_id, lead_id=lead_data.get("id"))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set initial status
        asyncio.run(redis_client.hset(
            f"lead:scoring:{task_id}",
            mapping={
                "status": "processing",
                "started_at": datetime.utcnow().isoformat(),
                "lead_id": lead_data.get("id", "unknown"),
                "company": lead_data.get("company", "Unknown")
            }
        ))
        
        # Initialize scoring components
        dynex_client = DynexClient()
        
        # Extract scoring factors
        company_size = lead_data.get("company_size", "unknown")
        industry = lead_data.get("industry", "unknown")
        budget = lead_data.get("budget", 0)
        timeline = lead_data.get("timeline", "unknown")
        engagement_level = lead_data.get("engagement_level", 0)
        
        # Quantum-enhanced scoring algorithm
        base_score = 50
        
        # Company size scoring
        size_scores = {
            "enterprise": 25,
            "large": 20,
            "medium": 15,
            "small": 10,
            "startup": 5
        }
        base_score += size_scores.get(company_size.lower(), 5)
        
        # Industry scoring
        high_value_industries = ["finance", "healthcare", "technology", "manufacturing"]
        if industry.lower() in high_value_industries:
            base_score += 15
        else:
            base_score += 5
        
        # Budget scoring
        if budget >= 100000:
            base_score += 20
        elif budget >= 50000:
            base_score += 15
        elif budget >= 10000:
            base_score += 10
        else:
            base_score += 5
        
        # Timeline urgency
        timeline_scores = {
            "immediate": 15,
            "1-3 months": 12,
            "3-6 months": 8,
            "6+ months": 3
        }
        base_score += timeline_scores.get(timeline.lower(), 3)
        
        # Engagement level
        base_score += min(engagement_level * 2, 15)
        
        # Apply quantum enhancement (simulated)
        quantum_factor = 1 + (hash(str(lead_data)) % 20) / 100  # 0-19% boost
        final_score = min(int(base_score * quantum_factor), 100)
        
        # Determine lead quality
        if final_score >= 80:
            quality = "hot"
            priority = "high"
        elif final_score >= 60:
            quality = "warm"
            priority = "medium"
        elif final_score >= 40:
            quality = "cold"
            priority = "low"
        else:
            quality = "unqualified"
            priority = "none"
        
        # Generate recommendations
        recommendations = []
        if final_score >= 70:
            recommendations.append("Schedule immediate follow-up call")
            recommendations.append("Assign to senior sales representative")
        elif final_score >= 50:
            recommendations.append("Send personalized proposal")
            recommendations.append("Schedule demo within 1 week")
        else:
            recommendations.append("Add to nurture campaign")
            recommendations.append("Follow up in 30 days")
        
        # Simulate processing time
        time.sleep(1 + (final_score / 100))  # 1-2 seconds based on score
        
        scoring_result = {
            "lead_id": lead_data.get("id"),
            "score": final_score,
            "quality": quality,
            "priority": priority,
            "quantum_enhancement": f"{((quantum_factor - 1) * 100):.1f}%",
            "scoring_factors": {
                "company_size": company_size,
                "industry": industry,
                "budget": budget,
                "timeline": timeline,
                "engagement_level": engagement_level
            },
            "recommendations": recommendations,
            "scored_at": datetime.utcnow().isoformat()
        }
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "score": final_score,
            "quality": quality,
            "result": json.dumps(scoring_result)
        }
        
        asyncio.run(redis_client.hset(
            f"lead:scoring:{task_id}",
            mapping=completion_data
        ))
        
        # Publish scoring event
        asyncio.run(redis_client.publish(
            "lead:updates",
            json.dumps({
                "task_id": task_id,
                "lead_id": lead_data.get("id"),
                "status": "scored",
                "score": final_score,
                "quality": quality,
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("Lead scoring completed", task_id=task_id, score=final_score, quality=quality)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "scoring_result": scoring_result
        }
        
    except Exception as e:
        logger.error("Lead scoring failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"lead:scoring:{task_id}",
            mapping=error_data
        ))
        
        raise

@celery_app.task(bind=True, name="leads.batch_score")
def batch_score_leads(self, leads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Score multiple leads in batch
    
    Args:
        leads_data: List of lead dictionaries
        
    Returns:
        Batch scoring results
    """
    task_id = self.request.id
    logger.info("Starting batch lead scoring", task_id=task_id, batch_size=len(leads_data))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set initial batch status
        asyncio.run(redis_client.hset(
            f"lead:batch:{task_id}",
            mapping={
                "status": "processing",
                "started_at": datetime.utcnow().isoformat(),
                "total_leads": len(leads_data),
                "completed_leads": 0
            }
        ))
        
        results = []
        
        for i, lead_data in enumerate(leads_data):
            try:
                # Score individual lead (reuse logic from score_lead_async)
                scoring_task = score_lead_async.apply_async(args=[lead_data])
                result = scoring_task.get(timeout=30)  # 30 second timeout
                
                results.append({
                    "lead_index": i,
                    "lead_id": lead_data.get("id"),
                    "status": "success",
                    "scoring_result": result["scoring_result"]
                })
                
                # Update progress
                asyncio.run(redis_client.hset(
                    f"lead:batch:{task_id}",
                    "completed_leads", i + 1
                ))
                
            except Exception as e:
                logger.error("Batch lead scoring failed", task_id=task_id, lead_index=i, error=str(e))
                results.append({
                    "lead_index": i,
                    "lead_id": lead_data.get("id"),
                    "status": "failed",
                    "error": str(e)
                })
        
        # Calculate batch statistics
        successful_scores = [r for r in results if r["status"] == "success"]
        failed_scores = [r for r in results if r["status"] == "failed"]
        
        if successful_scores:
            avg_score = sum(r["scoring_result"]["score"] for r in successful_scores) / len(successful_scores)
            quality_distribution = {}
            for result in successful_scores:
                quality = result["scoring_result"]["quality"]
                quality_distribution[quality] = quality_distribution.get(quality, 0) + 1
        else:
            avg_score = 0
            quality_distribution = {}
        
        batch_result = {
            "task_id": task_id,
            "status": "completed",
            "total_leads": len(leads_data),
            "successful_scores": len(successful_scores),
            "failed_scores": len(failed_scores),
            "average_score": avg_score,
            "quality_distribution": quality_distribution,
            "results": results,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "successful_scores": len(successful_scores),
            "failed_scores": len(failed_scores),
            "average_score": avg_score,
            "result": json.dumps(batch_result)
        }
        
        asyncio.run(redis_client.hset(
            f"lead:batch:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Batch lead scoring completed", task_id=task_id, 
                   successful=len(successful_scores), failed=len(failed_scores))
        
        return batch_result
        
    except Exception as e:
        logger.error("Batch lead scoring failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="leads.enrich_lead")
def enrich_lead_data(self, lead_id: str, enrichment_sources: List[str]) -> Dict[str, Any]:
    """
    Enrich lead data from external sources
    
    Args:
        lead_id: Lead identifier
        enrichment_sources: List of data sources to use
        
    Returns:
        Enriched lead data
    """
    task_id = self.request.id
    logger.info("Starting lead enrichment", task_id=task_id, lead_id=lead_id)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"lead:enrichment:{task_id}",
            mapping={
                "status": "enriching",
                "started_at": datetime.utcnow().isoformat(),
                "lead_id": lead_id,
                "sources": ",".join(enrichment_sources)
            }
        ))
        
        enriched_data = {}
        
        # Simulate enrichment from various sources
        for source in enrichment_sources:
            time.sleep(0.5)  # Simulate API call delay
            
            if source == "linkedin":
                enriched_data["linkedin"] = {
                    "company_employees": 1000 + (hash(lead_id) % 5000),
                    "industry_connections": 50 + (hash(lead_id) % 200),
                    "recent_posts": 5 + (hash(lead_id) % 10)
                }
            elif source == "clearbit":
                enriched_data["clearbit"] = {
                    "annual_revenue": f"${(hash(lead_id) % 50 + 10)}M",
                    "technology_stack": ["Salesforce", "HubSpot", "AWS"],
                    "funding_stage": "Series B"
                }
            elif source == "zoominfo":
                enriched_data["zoominfo"] = {
                    "contact_count": 10 + (hash(lead_id) % 50),
                    "decision_makers": 3 + (hash(lead_id) % 8),
                    "intent_signals": ["CRM Software", "Business Intelligence"]
                }
        
        # Calculate enrichment score
        enrichment_score = min(len(enriched_data) * 25, 100)
        
        enrichment_result = {
            "lead_id": lead_id,
            "enrichment_score": enrichment_score,
            "sources_used": enrichment_sources,
            "enriched_data": enriched_data,
            "enriched_at": datetime.utcnow().isoformat()
        }
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "enrichment_score": enrichment_score,
            "result": json.dumps(enrichment_result)
        }
        
        asyncio.run(redis_client.hset(
            f"lead:enrichment:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Lead enrichment completed", task_id=task_id, 
                   lead_id=lead_id, enrichment_score=enrichment_score)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "enrichment_result": enrichment_result
        }
        
    except Exception as e:
        logger.error("Lead enrichment failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="leads.generate_insights")
def generate_lead_insights(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate AI-powered insights for a lead
    
    Args:
        lead_data: Complete lead information
        
    Returns:
        Generated insights and recommendations
    """
    task_id = self.request.id
    logger.info("Starting lead insights generation", task_id=task_id)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"lead:insights:{task_id}",
            mapping={
                "status": "analyzing",
                "started_at": datetime.utcnow().isoformat(),
                "lead_id": lead_data.get("id", "unknown")
            }
        ))
        
        # Simulate AI analysis
        time.sleep(2)
        
        # Generate insights based on lead data
        insights = {
            "behavioral_patterns": [
                "High engagement with technical content",
                "Frequent visits to pricing page",
                "Downloaded multiple whitepapers"
            ],
            "buying_signals": [
                "Researching competitors actively",
                "Budget approved for Q1",
                "Technical evaluation in progress"
            ],
            "risk_factors": [
                "Long sales cycle typical for industry",
                "Multiple decision makers involved",
                "Budget constraints possible"
            ],
            "recommended_actions": [
                "Schedule technical demo",
                "Provide ROI calculator",
                "Connect with technical team"
            ],
            "next_best_action": "Send personalized technical proposal within 48 hours",
            "confidence_score": 0.75 + (hash(str(lead_data)) % 25) / 100
        }
        
        insights_result = {
            "lead_id": lead_data.get("id"),
            "insights": insights,
            "generated_at": datetime.utcnow().isoformat(),
            "ai_model": "Quantum-Enhanced Lead Intelligence v2.0"
        }
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "confidence_score": insights["confidence_score"],
            "result": json.dumps(insights_result)
        }
        
        asyncio.run(redis_client.hset(
            f"lead:insights:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Lead insights generation completed", task_id=task_id)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "insights_result": insights_result
        }
        
    except Exception as e:
        logger.error("Lead insights generation failed", task_id=task_id, error=str(e))
        raise