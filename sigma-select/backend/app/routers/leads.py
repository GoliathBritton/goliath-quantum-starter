from fastapi import APIRouter
from ..schemas.common import LeadScoreRequest, LeadScoreResponse
from ..services import leadgen

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/quantum-scoring", response_model=LeadScoreResponse)
def quantum_scoring(req: LeadScoreRequest):
    return leadgen.score_lead(req)
