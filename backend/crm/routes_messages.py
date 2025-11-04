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


router = APIRouter(tags=["CRM - Messages"])

class SendMessageIn(BaseModel):
    channel: str  # email|sms
    to: str
    subject: Optional[str] = None
    body: str

@router.get("/messages")
def list_messages(thread_id: Optional[str]=None, x_tenant_id: str = Depends(require_tenant)):
    return {"items":[{"id":"m_001","channel":"email","direction":"out","subject":"Welcome","body":"Hi there","created_at":now_iso()}]}

@router.post("/messages/send")
def send_message(payload: SendMessageIn, x_tenant_id: str = Depends(require_tenant)):
    return {"status":"sent","messageId":"m_"+uuid.uuid4().hex[:8]}
