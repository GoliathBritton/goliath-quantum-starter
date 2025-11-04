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


router = APIRouter(tags=["CRM - Contacts"])

class ContactIn(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    tags: Optional[List[str]] = []
    source: Optional[str] = None
    custom_json: Optional[Dict[str, Any]] = {}

@router.get("/contacts")
def list_contacts(q: Optional[str]=None, tags: Optional[str]=None, owner: Optional[str]=None, x_tenant_id: str = Depends(require_tenant)):
    return {"items":[
        {"id":"c_001","first_name":"Alex","last_name":"Quinn","email":"alex@example.com","score":79,"tags":["prospect"],"updated_at":now_iso()},
        {"id":"c_002","first_name":"Sam","last_name":"Lee","email":"sam@example.com","score":61,"tags":["newsletter"],"updated_at":now_iso()}
    ],"total":2}

@router.post("/contacts")
def create_contact(payload: ContactIn, x_tenant_id: str = Depends(require_tenant)):
    return {"id": "c_" + uuid.uuid4().hex[:8], "created_at": now_iso(), **payload.dict()}

@router.patch("/contacts/{contact_id}")
def update_contact(contact_id: str, payload: Dict[str, Any], x_tenant_id: str = Depends(require_tenant)):
    return {"id": contact_id, "updated_at": now_iso(), **payload}

@router.post("/contacts/{contact_id}/merge")
def merge_contact(contact_id: str, duplicate_id: str = Body(..., embed=True), x_tenant_id: str = Depends(require_tenant)):
    return {"id": contact_id, "merged": duplicate_id, "updated_at": now_iso()}

@router.post("/contacts/import")
def import_contacts(file: UploadFile = File(...), x_tenant_id: str = Depends(require_tenant)):
    return {"status": "queued", "jobId": "import_" + uuid.uuid4().hex[:8]}
