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


router = APIRouter(tags=["CRM - Reports"])

@router.get("/reports/pipeline")
def report_pipeline(x_tenant_id: str = Depends(require_tenant)):
    return {"pipelines":[{"name":"Default","stages":[
        {"stage":"Prospecting","value":75000},
        {"stage":"Demo","value":50000},
        {"stage":"Proposal","value":120000},
        {"stage":"Won","value":90000}
    ]}]}

@router.get("/reports/campaign-roi")
def report_campaign_roi(x_tenant_id: str = Depends(require_tenant)):
    return {"campaigns":[{"name":"Launch A","spend":5000,"revenue":25000},{"name":"Webinar","spend":2500,"revenue":12000}]}
