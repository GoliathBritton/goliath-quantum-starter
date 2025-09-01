from ..core.config import settings
from ..schemas.common import LeadScoreRequest, LeadScoreResponse
from math import tanh


def score_lead(req: LeadScoreRequest) -> LeadScoreResponse:
    # Toy model: industry prior + signal sum, "quantum" boost
    industry_prior = {
        "finance": 0.75,
        "healthcare": 0.7,
        "software": 0.8,
        "manufacturing": 0.6,
    }.get(req.industry.lower(), 0.5)
    signal_sum = sum(req.signals.values())
    base = 0.4 * industry_prior + 0.6 * tanh(signal_sum / 10.0)
    mult = settings.quantum.performance_multiplier
    score = max(0.0, min(1.0, base * (1.0 + 0.01 * (mult / 100))))
    rationale = [
        f"Industry prior={industry_prior}",
        f"Signals={round(signal_sum, 3)}",
        f"Dynex boost x{mult}",
    ]
    return LeadScoreResponse(
        score=round(score, 4),
        rationale=rationale,
        quantum_backend=settings.quantum.preferred_backend,
        multiplier=mult,
    )
