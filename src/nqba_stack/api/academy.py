"""
FLYFOX Academy API Endpoints

Provides REST API access to FLYFOX Academy features including:
- Training program enrollment and progress tracking
- Certification issuance and verification
- Developer program access and marketplace integration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from ..auth import get_current_user, require_feature
from ..academy import AcademyManager, AcademyTier, CertificationLevel
from ..core.ltc_logger import LTCLogger
from ..auth.entitlements import EntitlementsEngine

router = APIRouter(prefix="/academy", tags=["FLYFOX Academy"])


# Pydantic models for API requests/responses
class EnrollmentRequest(BaseModel):
    path_id: str
    tier: AcademyTier


class ProgressUpdateRequest(BaseModel):
    path_id: str
    module_completion: float
    time_spent: int


class CertificateRequest(BaseModel):
    path_id: str
    level: CertificationLevel


class LearningPathResponse(BaseModel):
    id: str
    name: str
    description: str
    difficulty: str
    estimated_hours: int
    modules: List[Dict[str, Any]]


class UserProgressResponse(BaseModel):
    path_id: str
    completion_percentage: float
    time_spent_minutes: int
    assessments_passed: int
    total_assessments: int
    certificate_earned: Optional[str]


class AcademyMetricsResponse(BaseModel):
    total_enrollments: int
    active_learners: int
    certification_completions: int
    developer_onboardings: int
    marketplace_contributions: int
    revenue_mrr: float
    satisfaction_score: float


# Dependency injection
async def get_academy_manager() -> AcademyManager:
    """Get the academy manager instance."""
    # This would be initialized in your main app startup
    ltc_logger = LTCLogger()
    entitlements = EntitlementsEngine()
    academy_manager = AcademyManager(ltc_logger, entitlements)
    await academy_manager.initialize_academy()
    return academy_manager


@router.get("/learning-paths", response_model=List[LearningPathResponse])
async def get_learning_paths(
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Get all available learning paths."""
    try:
        paths = list(academy_manager.learning_paths.values())
        return [
            LearningPathResponse(
                id=path.id,
                name=path.name,
                description=path.description,
                difficulty=path.difficulty,
                estimated_hours=path.estimated_hours,
                modules=[
                    {
                        "id": module.id,
                        "name": module.name,
                        "description": module.description,
                        "duration_minutes": module.duration_minutes,
                        "content_type": module.content_type,
                    }
                    for module in path.modules
                ],
            )
            for path in paths
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve learning paths: {str(e)}",
        )


@router.post("/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_in_path(
    request: EnrollmentRequest,
    current_user: dict = Depends(get_current_user),
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Enroll a user in a learning path."""
    try:
        success = await academy_manager.enroll_user(
            user_id=current_user["user_id"], path_id=request.path_id, tier=request.tier
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to enroll in learning path",
            )

        return {
            "message": "Successfully enrolled in learning path",
            "path_id": request.path_id,
            "tier": request.tier.value,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enrollment failed: {str(e)}",
        )


@router.put("/progress")
async def update_progress(
    request: ProgressUpdateRequest,
    current_user: dict = Depends(get_current_user),
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Update user progress in a learning path."""
    try:
        success = await academy_manager.track_progress(
            user_id=current_user["user_id"],
            path_id=request.path_id,
            module_completion=request.module_completion,
            time_spent=request.time_spent,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update progress",
            )

        return {
            "message": "Progress updated successfully",
            "path_id": request.path_id,
            "completion": request.module_completion,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Progress update failed: {str(e)}",
        )


@router.get("/progress", response_model=List[UserProgressResponse])
async def get_user_progress(
    current_user: dict = Depends(get_current_user),
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Get all learning progress for the current user."""
    try:
        progress = await academy_manager.get_user_progress(current_user["user_id"])

        return [
            UserProgressResponse(
                path_id=path_id,
                completion_percentage=prog.completion_percentage,
                time_spent_minutes=prog.time_spent_minutes,
                assessments_passed=prog.assessments_passed,
                total_assessments=prog.total_assessments,
                certificate_earned=prog.certificate_earned,
            )
            for path_id, prog in progress.items()
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve progress: {str(e)}",
        )


@router.post("/certificate", status_code=status.HTTP_201_CREATED)
async def request_certificate(
    request: CertificateRequest,
    current_user: dict = Depends(get_current_user),
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Request a certificate for a completed learning path."""
    try:
        certificate_id = await academy_manager.issue_certificate(
            user_id=current_user["user_id"],
            path_id=request.path_id,
            level=request.level,
        )

        if not certificate_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot issue certificate - path not completed",
            )

        return {
            "message": "Certificate issued successfully",
            "certificate_id": certificate_id,
            "path_id": request.path_id,
            "level": request.level.value,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Certificate issuance failed: {str(e)}",
        )


@router.get("/certificates/{certificate_id}")
async def get_certificate(
    certificate_id: str,
    current_user: dict = Depends(get_current_user),
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Get certificate details by ID."""
    try:
        certificate = academy_manager.certificates_issued.get(certificate_id)

        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
            )

        # Verify user owns this certificate
        if certificate.user_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this certificate",
            )

        return {
            "certificate_id": certificate.id,
            "path_id": certificate.path_id,
            "level": certificate.level.value,
            "issued_date": certificate.issued_date.isoformat(),
            "expiry_date": certificate.expiry_date.isoformat(),
            "metadata": certificate.metadata,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve certificate: {str(e)}",
        )


@router.get("/metrics", response_model=AcademyMetricsResponse)
@require_feature("ACADEMY_ADMIN")
async def get_academy_metrics(
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Get academy performance metrics (admin only)."""
    try:
        metrics = await academy_manager.get_academy_metrics()

        return AcademyMetricsResponse(
            total_enrollments=metrics.total_enrollments,
            active_learners=metrics.active_learners,
            certification_completions=metrics.certification_completions,
            developer_onboardings=metrics.developer_onboardings,
            marketplace_contributions=metrics.marketplace_contributions,
            revenue_mrr=metrics.revenue_mrr,
            satisfaction_score=metrics.satisfaction_score,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}",
        )


@router.get("/health")
async def academy_health_check(
    academy_manager: AcademyManager = Depends(get_academy_manager),
):
    """Health check for the academy system."""
    try:
        # Check if academy is properly initialized
        if not academy_manager.learning_paths:
            raise Exception("No learning paths loaded")

        return {
            "status": "healthy",
            "learning_paths": len(academy_manager.learning_paths),
            "registered_agents": len(academy_manager.agent_capabilities),
            "active_enrollments": sum(
                len(enrollments)
                for enrollments in academy_manager.active_enrollments.values()
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Academy system unhealthy: {str(e)}",
        )
