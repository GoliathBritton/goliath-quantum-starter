from fastapi import APIRouter
from ..schemas.common import QEIRequest, QEIResponse, MomentumRequest, MomentumResponse
from ..services import sigmaeq

router = APIRouter(prefix="/sigmaeq", tags=["sigmaeq"])


@router.post("/qei-calculation", response_model=QEIResponse)
def qei(req: QEIRequest):
    return sigmaeq.qei_calculation(req)


@router.post("/momentum-tracking", response_model=MomentumResponse)
def momentum(req: MomentumRequest):
    return sigmaeq.momentum_tracking(req)
