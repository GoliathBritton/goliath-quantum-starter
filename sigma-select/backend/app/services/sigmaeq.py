from ..core.config import settings
from ..schemas.common import QEIRequest, QEIResponse, MomentumRequest, MomentumResponse
from math import tanh


def _dynex_multiplier() -> float:
    return settings.quantum.performance_multiplier


def qei_calculation(req: QEIRequest) -> QEIResponse:
    # Simple normalized composite index (placeholder). Replace with QUBO in prod.
    weights = {
        "cycle_time": 0.25,
        "win_rate": 0.3,
        "acv": 0.25,
        "cac": -0.2,
        "ltv": 0.2,
    }
    base = 0.0
    drivers = {}
    for k, w in weights.items():
        v = float(req.inputs.get(k, 0))
        c = w * tanh(v / 100.0)
        drivers[k] = c
        base += c
    qei = max(0.0, min(1.0, 0.5 + base))  # clamp 0..1
    mult = _dynex_multiplier()
    boosted = max(
        0.0, min(1.0, qei * (1.0 + 0.01 * (mult / 100)))
    )  # gentle "quantum boost"
    return QEIResponse(
        qei_score=round(boosted, 4),
        drivers={k: round(v, 4) for k, v in drivers.items()},
        window=req.window,
        quantum_backend=settings.quantum.preferred_backend,
        multiplier=mult,
    )


def momentum_tracking(req: MomentumRequest) -> MomentumResponse:
    # Velocity-esque composite
    weights = {"daily_wins": 0.5, "avg_deal_size": 0.3, "velocity": 0.2}
    m = sum(weights.get(k, 0) * float(v) for k, v in req.metrics.items())
    norm = tanh(m / 1000.0)
    contributors = {k: float(v) * weights.get(k, 0) for k, v in req.metrics.items()}
    return MomentumResponse(
        momentum=round(norm, 4), contributors=contributors, window=req.window
    )
