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


router = APIRouter(tags=["CRM - Tasks"])

class TaskIn(BaseModel):
    title: str
    due_at: Optional[str] = None
    owner_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    priority: Optional[str] = "normal"

@router.get("/tasks")
def list_tasks(x_tenant_id: str = Depends(require_tenant)):
    return {"items":[{"id":"t_001","title":"Follow up with Alex","status":"open","due_at":now_iso()}]}

@router.post("/tasks")
def create_task(payload: TaskIn, x_tenant_id: str = Depends(require_tenant)):
    return {"id":"t_"+uuid.uuid4().hex[:8], "status":"open", "created_at": now_iso(), **payload.dict()}
