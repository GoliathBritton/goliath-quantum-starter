"""Leads management router for NQBA Core API

Implements lead management endpoints according to the OpenAPI specification.
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import json
import csv
import io
from models import (
    Lead,
    LeadsListResponse,
    Pagination,
    ScoreResponse,
    ScoreFactor,
    TaskResponse,
    LeadStatus,
    ScoreImpact,
    TaskStatus,
    ErrorResponse
)
from auth_router import verify_token

# Create router
leads_router = APIRouter(prefix="/leads", tags=["leads"])

# Mock leads database (in production, use proper database)
MOCK_LEADS: Dict[str, Lead] = {}
MOCK_TASKS: Dict[str, TaskResponse] = {}


def generate_lead_id() -> str:
    """Generate a unique lead ID"""
    return f"lead_{uuid.uuid4().hex[:8]}"


def generate_task_id() -> str:
    """Generate a unique task ID"""
    return f"task_{uuid.uuid4().hex[:8]}"


def get_lead_by_id(lead_id: str) -> Lead:
    """Get lead by ID or raise 404"""
    lead = MOCK_LEADS.get(lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return lead


def calculate_lead_score(lead: Lead) -> ScoreResponse:
    """Calculate a mock score for a lead"""
    # Mock scoring algorithm
    base_score = 50.0
    factors = []
    
    # Company factor
    if lead.company:
        company_score = min(len(lead.company) * 2, 20)
        base_score += company_score
        factors.append(ScoreFactor(
            name="Company Presence",
            weight=0.3,
            value=company_score,
            impact=ScoreImpact.positive
        ))
    
    # Email domain factor
    if lead.email and '@' in lead.email:
        domain = lead.email.split('@')[1]
        if domain in ['gmail.com', 'yahoo.com', 'hotmail.com']:
            domain_score = -10
            impact = ScoreImpact.negative
        else:
            domain_score = 15
            impact = ScoreImpact.positive
        
        base_score += domain_score
        factors.append(ScoreFactor(
            name="Email Domain",
            weight=0.2,
            value=abs(domain_score),
            impact=impact
        ))
    
    # Phone factor
    if lead.phone:
        phone_score = 10
        base_score += phone_score
        factors.append(ScoreFactor(
            name="Phone Available",
            weight=0.1,
            value=phone_score,
            impact=ScoreImpact.positive
        ))
    
    # Name factor
    if lead.name:
        name_score = 5
        base_score += name_score
        factors.append(ScoreFactor(
            name="Name Provided",
            weight=0.1,
            value=name_score,
            impact=ScoreImpact.positive
        ))
    
    # Ensure score is within bounds
    final_score = max(0, min(100, base_score))
    confidence = min(0.95, len(factors) * 0.2 + 0.3)
    
    return ScoreResponse(
        lead_id=lead.id,
        score=final_score,
        confidence=confidence,
        factors=factors,
        model_version="v1.0.0",
        scored_at=datetime.utcnow()
    )


@leads_router.post("/import")
async def import_leads(
    file: UploadFile = File(...),
    metadata: str = None,
    current_user: dict = Depends(verify_token)
):
    """Import leads from CSV or JSON file"""
    task_id = generate_task_id()
    
    # Create task response
    task = TaskResponse(
        task_id=task_id,
        status=TaskStatus.queued,
        created_at=datetime.utcnow(),
        estimated_completion=datetime.utcnow()
    )
    MOCK_TASKS[task_id] = task
    
    try:
        # Read file content
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            # Parse CSV
            csv_content = content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            imported_count = 0
            for row in csv_reader:
                lead_id = generate_lead_id()
                lead = Lead(
                    id=lead_id,
                    email=row.get('email', ''),
                    name=row.get('name'),
                    company=row.get('company'),
                    phone=row.get('phone'),
                    source=row.get('source', 'csv_import'),
                    created_at=datetime.utcnow(),
                    custom_fields={k: v for k, v in row.items() if k not in ['email', 'name', 'company', 'phone', 'source']}
                )
                MOCK_LEADS[lead_id] = lead
                imported_count += 1
        
        elif file.filename.endswith('.json'):
            # Parse JSON
            json_content = json.loads(content.decode('utf-8'))
            
            if isinstance(json_content, list):
                leads_data = json_content
            else:
                leads_data = [json_content]
            
            imported_count = 0
            for lead_data in leads_data:
                lead_id = generate_lead_id()
                lead = Lead(
                    id=lead_id,
                    email=lead_data.get('email', ''),
                    name=lead_data.get('name'),
                    company=lead_data.get('company'),
                    phone=lead_data.get('phone'),
                    source=lead_data.get('source', 'json_import'),
                    created_at=datetime.utcnow(),
                    custom_fields=lead_data.get('custom_fields', {})
                )
                MOCK_LEADS[lead_id] = lead
                imported_count += 1
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Please use CSV or JSON."
            )
        
        # Update task status
        task.status = TaskStatus.completed
        task.estimated_completion = datetime.utcnow()
        MOCK_TASKS[task_id] = task
        
        return {
            "task_id": task_id,
            "status": "completed",
            "imported_count": imported_count,
            "message": f"Successfully imported {imported_count} leads"
        }
    
    except Exception as e:
        # Update task status to failed
        task.status = TaskStatus.failed
        MOCK_TASKS[task_id] = task
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import leads: {str(e)}"
        )


@leads_router.get("/", response_model=LeadsListResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[LeadStatus] = None,
    current_user: dict = Depends(verify_token)
):
    """List leads with pagination and filtering"""
    leads = list(MOCK_LEADS.values())
    
    # Apply status filter
    if status:
        leads = [lead for lead in leads if lead.status == status]
    
    # Calculate pagination
    total = len(leads)
    pages = (total + limit - 1) // limit
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    paginated_leads = leads[start_idx:end_idx]
    
    return LeadsListResponse(
        leads=paginated_leads,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total,
            pages=pages
        )
    )


@leads_router.get("/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str, current_user: dict = Depends(verify_token)):
    """Get lead details"""
    return get_lead_by_id(lead_id)


@leads_router.get("/{lead_id}/score", response_model=ScoreResponse)
async def get_lead_score(lead_id: str, current_user: dict = Depends(verify_token)):
    """Get score for a lead"""
    lead = get_lead_by_id(lead_id)
    return calculate_lead_score(lead)


@leads_router.post("/{lead_id}/enrich")
async def enrich_lead(
    lead_id: str,
    current_user: dict = Depends(verify_token)
):
    """Enrich lead data with additional information"""
    lead = get_lead_by_id(lead_id)
    
    task_id = generate_task_id()
    
    # Create enrichment task
    task = TaskResponse(
        task_id=task_id,
        status=TaskStatus.running,
        created_at=datetime.utcnow(),
        estimated_completion=datetime.utcnow()
    )
    MOCK_TASKS[task_id] = task
    
    # Mock enrichment process (in production, this would be async)
    # Add some mock enriched data
    if not lead.custom_fields:
        lead.custom_fields = {}
    
    lead.custom_fields.update({
        "enriched_at": datetime.utcnow().isoformat(),
        "industry": "Technology",
        "company_size": "50-100 employees",
        "annual_revenue": "$5M-$10M",
        "social_profiles": {
            "linkedin": f"https://linkedin.com/company/{lead.company.lower().replace(' ', '-')}" if lead.company else None,
            "twitter": f"@{lead.company.lower().replace(' ', '')}" if lead.company else None
        }
    })
    
    # Update lead in storage
    MOCK_LEADS[lead_id] = lead
    
    # Mark task as completed
    task.status = TaskStatus.completed
    MOCK_TASKS[task_id] = task
    
    return task


@leads_router.put("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: str,
    lead_update: Lead,
    current_user: dict = Depends(verify_token)
):
    """Update lead information"""
    existing_lead = get_lead_by_id(lead_id)
    
    # Update fields
    if lead_update.name is not None:
        existing_lead.name = lead_update.name
    if lead_update.company is not None:
        existing_lead.company = lead_update.company
    if lead_update.phone is not None:
        existing_lead.phone = lead_update.phone
    if lead_update.status is not None:
        existing_lead.status = lead_update.status
    if lead_update.source is not None:
        existing_lead.source = lead_update.source
    if lead_update.custom_fields is not None:
        if existing_lead.custom_fields is None:
            existing_lead.custom_fields = {}
        existing_lead.custom_fields.update(lead_update.custom_fields)
    
    # Update in storage
    MOCK_LEADS[lead_id] = existing_lead
    
    return existing_lead


@leads_router.delete("/{lead_id}")
async def delete_lead(lead_id: str, current_user: dict = Depends(verify_token)):
    """Delete a lead"""
    if lead_id not in MOCK_LEADS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    del MOCK_LEADS[lead_id]
    
    return {"message": "Lead deleted successfully", "lead_id": lead_id}


@leads_router.get("/tasks/{task_id}")
async def get_task_status(task_id: str, current_user: dict = Depends(verify_token)):
    """Get status of an import or enrichment task"""
    task = MOCK_TASKS.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task