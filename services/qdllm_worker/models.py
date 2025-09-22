"""qdLLM Worker Data Models

Pydantic models for qdLLM worker requests, responses, and results.
"""

import time
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class QdLLMRequest(BaseModel):
    """Request model for qdLLM worker"""
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    request_type: str = Field(..., description="Type of qdLLM request")
    prompt: Optional[str] = Field(None, description="Main prompt for processing")
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Request parameters")
    priority: str = Field("normal", description="Request priority level")
    timeout: int = Field(30, description="Request timeout in seconds")
    created_at: float = Field(default_factory=time.time)
    
    class Config:
        schema_extra = {
            "example": {
                "request_type": "parallel_exploration",
                "context": {
                    "lead_profile": {
                        "name": "John Smith",
                        "company": "TechCorp",
                        "title": "VP Engineering"
                    },
                    "objective": "schedule_demo"
                },
                "parameters": {
                    "num_strategies": 6,
                    "constraints": ["professional_tone", "under_160_chars"]
                }
            }
        }


class QdLLMResponse(BaseModel):
    """Response model for qdLLM worker"""
    request_id: str
    result: Union[Dict[str, Any], List[Any], str]
    processing_time: float
    quantum_enhanced: bool = False
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)
    
    class Config:
        schema_extra = {
            "example": {
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "result": {
                    "strategies": [
                        {
                            "strategy_id": "S1",
                            "strategy_name": "Consultative Discovery",
                            "conversion_confidence": 0.85
                        }
                    ]
                },
                "processing_time": 2.34,
                "quantum_enhanced": True,
                "confidence": 0.92
            }
        }


class ExplorationResult(BaseModel):
    """Result model for parallel exploration"""
    strategies: List[Dict[str, Any]]
    quantum_ranked: bool = False
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "strategies": [
                    {
                        "strategy_id": "S1",
                        "strategy_name": "Consultative Discovery",
                        "core_approach": "consultative",
                        "opening_line": "Hi John, I noticed TechCorp is expanding. What's your biggest scaling challenge?",
                        "conversion_confidence": 0.85,
                        "ideal_prospect_fit": "Growth-stage companies with operational challenges"
                    },
                    {
                        "strategy_id": "S2",
                        "strategy_name": "Social Proof Approach",
                        "core_approach": "social_proof",
                        "opening_line": "Hi John, we helped similar companies like YourCompetitor reduce costs by 30%.",
                        "conversion_confidence": 0.78,
                        "ideal_prospect_fit": "Companies concerned about competitive positioning"
                    }
                ],
                "quantum_ranked": True,
                "confidence": 0.92,
                "metadata": {
                    "num_strategies": 2,
                    "objective": "schedule_demo",
                    "quantum_enhanced": True
                }
            }
        }


class ReasoningResult(BaseModel):
    """Result model for reversal reasoning"""
    analysis: Dict[str, Any]
    quantum_enhanced: bool = False
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "analysis": {
                    "analysis_metadata": {
                        "outcome_analyzed": "Sales forecast dropped 15%",
                        "analysis_timestamp": "2024-01-15T10:30:00Z",
                        "confidence_threshold": 0.7
                    },
                    "backtrace_candidates": [
                        {
                            "candidate_id": "C1",
                            "cause_summary": "Lead quality degradation from new marketing channels",
                            "supporting_evidence": ["Lower engagement rates", "Increased bounce rates"],
                            "likelihood_score": 0.85,
                            "confidence_level": "high",
                            "corrective_action": "Audit and optimize lead generation sources",
                            "verification_method": "A/B test original vs new channels"
                        }
                    ],
                    "synthesis": {
                        "primary_hypothesis": "Marketing channel quality issues",
                        "recommended_investigation_order": ["C1", "C2", "C3"]
                    }
                },
                "quantum_enhanced": True,
                "confidence": 0.88,
                "metadata": {
                    "outcome_analyzed": "Sales forecast dropped 15%",
                    "num_candidates": 6,
                    "quantum_optimized": True
                }
            }
        }


class RankingResult(BaseModel):
    """Result model for quantum ranking"""
    ranking: Dict[str, Any]
    quantum_optimized: bool = False
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "ranking": {
                    "ranking_metadata": {
                        "ranking_id": "QR_1642248600",
                        "optimization_goal": "maximize_conversion",
                        "candidate_count": 5
                    },
                    "quantum_ranking": [
                        {
                            "rank": 1,
                            "candidate_id": "lead_001",
                            "candidate_name": "TechCorp - John Smith",
                            "overall_score": 87.5,
                            "confidence_level": 0.92,
                            "dimension_scores": {
                                "fit_score": 90,
                                "engagement_score": 85,
                                "urgency_score": 88
                            }
                        }
                    ],
                    "ranking_analysis": {
                        "top_choice": {
                            "candidate_id": "lead_001",
                            "selection_rationale": "Highest overall fit and engagement",
                            "success_probability": 0.87
                        }
                    }
                },
                "quantum_optimized": True,
                "confidence": 0.91,
                "metadata": {
                    "num_candidates": 5,
                    "optimization_goal": "maximize_conversion",
                    "quantum_enhanced": True
                }
            }
        }


class LeadQualificationResult(BaseModel):
    """Result model for lead qualification"""
    qualification: Dict[str, Any]
    quantum_scored: bool = False
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "qualification": {
                    "qualification_metadata": {
                        "lead_id": "lead_001",
                        "company_name": "TechCorp",
                        "analysis_timestamp": "2024-01-15T10:30:00Z"
                    },
                    "overall_qualification": {
                        "composite_score": 78,
                        "qualification_tier": "A",
                        "priority_level": "high",
                        "recommended_action": "immediate_engagement"
                    },
                    "dimension_scores": {
                        "bant": {
                            "budget": {"score": 75, "confidence": 0.8},
                            "authority": {"score": 85, "confidence": 0.9},
                            "need": {"score": 90, "confidence": 0.95},
                            "timeline": {"score": 60, "confidence": 0.7}
                        },
                        "fit_score": {"score": 88, "confidence": 0.9},
                        "engagement_score": {"score": 72, "confidence": 0.8}
                    }
                },
                "quantum_scored": True,
                "confidence": 0.85,
                "metadata": {
                    "lead_id": "lead_001",
                    "qualification_version": "2.0",
                    "quantum_enhanced": True
                }
            }
        }


class WorkerMetrics(BaseModel):
    """Worker performance metrics"""
    requests_processed: int = 0
    parallel_explorations: int = 0
    reasoning_sessions: int = 0
    quantum_rankings: int = 0
    average_response_time: float = 0.0
    error_count: int = 0
    error_rate: float = 0.0
    uptime_seconds: float = 0.0
    quantum_enhancement_rate: float = 0.0
    
    class Config:
        schema_extra = {
            "example": {
                "requests_processed": 1247,
                "parallel_explorations": 423,
                "reasoning_sessions": 156,
                "quantum_rankings": 298,
                "average_response_time": 2.34,
                "error_count": 12,
                "error_rate": 0.0096,
                "uptime_seconds": 86400,
                "quantum_enhancement_rate": 0.87
            }
        }


class HealthStatus(BaseModel):
    """Worker health status"""
    status: str = "healthy"
    quantum_job_manager: bool = False
    prompts_loaded: int = 0
    requests_processed: int = 0
    error_rate: float = 0.0
    last_request_time: Optional[float] = None
    dependencies: Dict[str, bool] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "quantum_job_manager": True,
                "prompts_loaded": 4,
                "requests_processed": 1247,
                "error_rate": 0.0096,
                "last_request_time": 1642248600.123,
                "dependencies": {
                    "openai_api": True,
                    "dynex_sdk": True,
                    "quantum_job_manager": True
                }
            }
        }


class BatchRequest(BaseModel):
    """Batch processing request"""
    batch_id: str = Field(default_factory=lambda: str(uuid4()))
    requests: List[QdLLMRequest]
    batch_priority: str = Field("normal", description="Batch priority level")
    parallel_processing: bool = Field(True, description="Process requests in parallel")
    max_concurrency: int = Field(5, description="Maximum concurrent requests")
    timeout: int = Field(60, description="Batch timeout in seconds")
    created_at: float = Field(default_factory=time.time)
    
    class Config:
        schema_extra = {
            "example": {
                "requests": [
                    {
                        "request_type": "parallel_exploration",
                        "context": {"objective": "schedule_demo"}
                    },
                    {
                        "request_type": "lead_qualification",
                        "context": {"lead_data": {"company": "TechCorp"}}
                    }
                ],
                "batch_priority": "high",
                "parallel_processing": True,
                "max_concurrency": 3
            }
        }


class BatchResponse(BaseModel):
    """Batch processing response"""
    batch_id: str
    responses: List[QdLLMResponse]
    total_processing_time: float
    successful_requests: int
    failed_requests: int
    batch_success_rate: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)
    
    class Config:
        schema_extra = {
            "example": {
                "batch_id": "batch_123e4567-e89b-12d3-a456-426614174000",
                "responses": [],
                "total_processing_time": 5.67,
                "successful_requests": 8,
                "failed_requests": 2,
                "batch_success_rate": 0.8,
                "metadata": {
                    "parallel_processing": True,
                    "max_concurrency": 5
                }
            }
        }


# Request type constants
class RequestTypes:
    """Constants for qdLLM request types"""
    PARALLEL_EXPLORATION = "parallel_exploration"
    REVERSAL_REASONING = "reversal_reasoning"
    QUANTUM_RANKING = "quantum_ranking"
    LEAD_QUALIFICATION = "lead_qualification"
    GENERAL_COMPLETION = "general_completion"
    BATCH_PROCESSING = "batch_processing"


# Priority levels
class PriorityLevels:
    """Constants for request priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# Status constants
class StatusTypes:
    """Constants for status types"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    MAINTENANCE = "maintenance"