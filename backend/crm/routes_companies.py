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


router = APIRouter(tags=["CRM - Companies"])

class CompanyIn(BaseModel):
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    owner_id: Optional[str] = None
    tags: Optional[List[str]] = []

@router.get("/companies")
def list_companies(q: Optional[str]=None, x_tenant_id: str = Depends(require_tenant)):
    return {"items":[{"id":"co_001","name":"Quantum Co","domain":"quantum.example","industry":"SaaS","updated_at":now_iso()}],"total":1}

@router.post("/companies")
def create_company(payload: CompanyIn, x_tenant_id: str = Depends(require_tenant)):
    return {"id":"co_"+uuid.uuid4().hex[:8], "created_at": now_iso(), **payload.dict()}
