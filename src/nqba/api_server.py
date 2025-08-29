from fastapi import FastAPI, Header, HTTPException, Path, Body
from pydantic import BaseModel
from .decision_logic import decide
from .quantum_adapter import optimize_qubo
from .ltc_logger import ltc_record
from .neuromorphic_automations import AUTOMATIONS

app = FastAPI(title="NQBA Core", version="0.1.0")
from typing import Any


class AutomationRequest(BaseModel):
    args: list[Any] = []
    kwargs: dict = {}


@app.post("/v1/automation/{name}")
def run_automation(
    name: str = Path(..., description="Automation name"),
    req: AutomationRequest = Body(...),
):
    if name not in AUTOMATIONS:
        raise HTTPException(status_code=404, detail=f"Automation '{name}' not found")
    try:
        result = AUTOMATIONS[name](*req.args, **req.kwargs)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DecideRequest(BaseModel):
    policy_id: str
    features: dict


class DecideResponse(BaseModel):
    decision_id: str
    result: dict
    explanation: str
    ltc_ref: str


class QuboRequest(BaseModel):
    variables: int
    Q: list
    constraints: list = []
    objective: str = "maximize"


class OptimizeResponse(BaseModel):
    decision_id: str
    assignment: list
    objective_value: float
    backend: str
    ltc_ref: str


def _auth(api_key: str | None):
    # Sprint-1: simple header check; replace with OAuth later
    expected = None  # set via env or config if desired
    if expected and api_key != expected:
        raise HTTPException(status_code=401, detail="unauthorized")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/v1/decide", response_model=DecideResponse)
def post_decide(req: DecideRequest, x_api_key: str | None = Header(default=None)):
    _auth(x_api_key)
    decision = decide(req.policy_id, req.features)
    ltc = ltc_record(
        policy_id=req.policy_id,
        inputs={"features": req.features},
        outputs=decision["result"],
        explanation=decision["explanation"],
        solver_backend="decision.logic",
    )
    return {
        "decision_id": decision["decision_id"],
        "result": decision["result"],
        "explanation": decision["explanation"],
        "ltc_ref": ltc["ltc_id"],
    }


@app.post("/v1/optimize", response_model=OptimizeResponse)
def post_optimize(req: QuboRequest, x_api_key: str | None = Header(default=None)):
    _auth(x_api_key)
    out = optimize_qubo(req.variables, req.Q, req.constraints, req.objective)
    ltc = ltc_record(
        policy_id="optimize.qubo",
        inputs={"variables": req.variables},
        outputs={
            "assignment": out["assignment"],
            "objective_value": out["objective_value"],
        },
        explanation="QUBO optimization (heuristic)",
        solver_backend=out["backend"],
    )
    return {
        "decision_id": out["decision_id"],
        "assignment": out["assignment"],
        "objective_value": out["objective_value"],
        "backend": out["backend"],
        "ltc_ref": ltc["ltc_id"],
    }
