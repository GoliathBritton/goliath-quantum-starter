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


router = APIRouter(tags=["CRM - Automations"])

@router.post("/automations")
def define_automation(recipe: Dict[str, Any], x_tenant_id: str = Depends(require_tenant)):
    return {"id": "a_"+uuid.uuid4().hex[:8], "saved": True, "recipe": recipe}

@router.post("/automations/run")
def run_automation(payload: Dict[str, Any], x_tenant_id: str = Depends(require_tenant)):
    return {"status":"running","runId":"run_"+uuid.uuid4().hex[:8]}
