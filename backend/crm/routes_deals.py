from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, File, Body
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import uuid, datetime

def require_tenant(x_tenant_id: Optional[str] = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-Id")
    return x_tenant_id

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


router = APIRouter(tags=["CRM - Deals"])

class DealIn(BaseModel):
    title: str
    company_id: Optional[str] = None
    contact_id: Optional[str] = None
    pipeline_id: Optional[str] = "p_default"
    stage: Optional[str] = "Prospecting"
    amount: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    close_date: Optional[str] = None
    owner_id: Optional[str] = None

@router.get("/deals")
def list_deals(pipeline: Optional[str]="p_default", x_tenant_id: str = Depends(require_tenant)):
    return {"items":[
        {"id":"d_001","title":"Pilot - Quantum Co","stage":"Prospecting","amount":15000,"pipeline_id":pipeline},
        {"id":"d_002","title":"NQBA Sentinel","stage":"Demo","amount":50000,"pipeline_id":pipeline}
    ],"total":2}

@router.post("/deals")
def create_deal(payload: DealIn, x_tenant_id: str = Depends(require_tenant)):
    return {"id":"d_"+uuid.uuid4().hex[:8], "created_at":now_iso(), **payload.dict()}

@router.patch("/deals/{deal_id}")
def update_deal(deal_id: str, payload: Dict[str, Any], x_tenant_id: str = Depends(require_tenant)):
    return {"id":deal_id, "updated_at": now_iso(), **payload}
