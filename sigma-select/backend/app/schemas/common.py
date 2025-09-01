from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class QEIRequest(BaseModel):
    inputs: Dict[str, float]  # e.g., cycle_time, win_rate, acv, cac, ltv
    window: str = "7d"


class QEIResponse(BaseModel):
    qei_score: float
    drivers: Dict[str, float]
    window: str
    quantum_backend: str
    multiplier: float


class LeadScoreRequest(BaseModel):
    company: str
    industry: str
    signals: Dict[str, float]


class LeadScoreResponse(BaseModel):
    score: float
    rationale: List[str]
    quantum_backend: str
    multiplier: float


class MomentumRequest(BaseModel):
    metrics: Dict[str, float]  # e.g., daily_wins, avg_deal_size, velocity
    window: str = "7d"


class MomentumResponse(BaseModel):
    momentum: float
    contributors: Dict[str, float]
    window: str
