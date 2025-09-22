import asyncio
import logging
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib

try:
    import redis.asyncio as redis
except ImportError:
    print("Warning: Redis library not installed. Install with: pip install redis")
    redis = None

# Enums
class EthicsLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"

class ComplianceFramework(Enum):
    GDPR = "gdpr"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    SOX = "sox"
    TCPA = "tcpa"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"
    NIST = "nist"

class ActionType(Enum):
    CONVERSATION = "conversation"
    PHONE_CALL = "phone_call"
    DATA_ACCESS = "data_access"
    DECISION_MAKING = "decision_making"
    AUTOMATION = "automation"
    ESCALATION = "escalation"

@dataclass
class EthicsRequest:
    """Request for ethics review"""
    request_id: str
    agent_id: str
    action_type: ActionType
    content: str
    context: Dict[str, Any]
    risk_factors: List[str]
    compliance_requirements: List[ComplianceFramework]
    priority: EthicsLevel
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: Optional[str] = None

@dataclass
class EthicsResponse:
    """Response from ethics review"""
    request_id: str
    status: ReviewStatus
    approved: bool
    confidence: float
    rationale: str
    recommendations: List[str]
    compliance_status: Dict[ComplianceFramework, bool]
    risk_score: float
    human_review_required: bool
    expiry_time: Optional[str] = None
    reviewer_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ComplianceRule:
    """Compliance rule definition"""
    rule_id: str
    framework: ComplianceFramework
    name: str
    description: str
    severity: EthicsLevel
    conditions: Dict[str, Any]
    actions: List[str]
    enabled: bool = True

@dataclass
class AuditLog:
    """Audit log entry"""
    log_id: str
    timestamp: str
    agent_id: str
    action_type: ActionType
    request_id: str
    decision: str
    rationale: str
    compliance_frameworks: List[ComplianceFramework]
    risk_score: float
    human_reviewer: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class QHCGovernance:
    """Quantum High Council (QHC) Governance Service for Ethics and Compliance"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Redis connection for caching and session management
        self.redis_client = None
        if redis and self.config.get("redis_url"):
            self.redis_client = redis.from_url(self.config["redis_url"])
        
        # Compliance rules registry
        self.compliance_rules: Dict[str, ComplianceRule] = {}
        
        # Ethics review cache
        self.ethics_cache: Dict[str, EthicsResponse] = {}
        
        # Audit logging
        self.audit_logs: List[AuditLog] = []
        
        # Human reviewers queue
        self.human_review_queue: List[EthicsRequest] = []
        
        # Performance metrics
        self.total_reviews = 0
        self.auto_approved = 0
        self.human_reviews = 0
        self.compliance_violations = 0
        
        # Risk scoring weights
        self.risk_weights = {
            "pii_exposure": 0.3,
            "financial_impact": 0.25,
            "regulatory_risk": 0.2,
            "reputation_risk": 0.15,
            "operational_risk": 0.1
        }
        
        self.logger.info("QHC Governance Service initialized")
    
    async def initialize(self):
        """Initialize the QHC Governance service"""
        try:
            # Test Redis connectivity
            if self.redis_client:
                await self.redis_client.ping()
                self.logger.info("Redis connectivity confirmed")
            
            # Load compliance rules
            await self._load_compliance_rules()
            
            # Initialize audit logging
            await self._initialize_audit_logging()
            
            self.logger.info("QHC Governance Service initialization complete")
            
        except Exception as e:
            self.logger.error(f"QHC Governance Service initialization failed: {e}")
            raise
    
    async def _load_compliance_rules(self):
        """Load compliance rules from configuration"""
        # GDPR Rules
        self.compliance_rules["gdpr_consent"] = ComplianceRule(
            rule_id="gdpr_consent",
            framework=ComplianceFramework.GDPR,
            name="GDPR Consent Verification",
            description="Ensure explicit consent for data processing",
            severity=EthicsLevel.HIGH,
            conditions={"requires_consent": True, "data_processing": True},
            actions=["verify_consent", "log_processing", "enable_deletion"]
        )
        
        self.compliance_rules["gdpr_data_minimization"] = ComplianceRule(
            rule_id="gdpr_data_minimization",
            framework=ComplianceFramework.GDPR,
            name="GDPR Data Minimization",
            description="Collect only necessary personal data",
            severity=EthicsLevel.MEDIUM,
            conditions={"personal_data": True},
            actions=["minimize_collection", "justify_necessity"]
        )
        
        # TCPA Rules
        self.compliance_rules["tcpa_consent"] = ComplianceRule(
            rule_id="tcpa_consent",
            framework=ComplianceFramework.TCPA,
            name="TCPA Call Consent",
            description="Verify consent for automated calls",
            severity=EthicsLevel.CRITICAL,
            conditions={"automated_call": True},
            actions=["verify_consent", "maintain_dnc_list", "log_consent"]
        )
        
        # HIPAA Rules
        self.compliance_rules["hipaa_phi"] = ComplianceRule(
            rule_id="hipaa_phi",
            framework=ComplianceFramework.HIPAA,
            name="HIPAA PHI Protection",
            description="Protect Personal Health Information",
            severity=EthicsLevel.CRITICAL,
            conditions={"health_data": True},
            actions=["encrypt_data", "access_control", "audit_access"]
        )
        
        # PCI DSS Rules
        self.compliance_rules["pci_card_data"] = ComplianceRule(
            rule_id="pci_card_data",
            framework=ComplianceFramework.PCI_DSS,
            name="PCI DSS Card Data Protection",
            description="Protect cardholder data",
            severity=EthicsLevel.CRITICAL,
            conditions={"payment_data": True},
            actions=["encrypt_storage", "secure_transmission", "access_control"]
        )
        
        self.logger.info(f"Loaded {len(self.compliance_rules)} compliance rules")
    
    async def _initialize_audit_logging(self):
        """Initialize audit logging system"""
        # In production, this would connect to a secure audit database
        self.logger.info("Audit logging system initialized")
    
    async def request_ethics_review(self, request: EthicsRequest) -> EthicsResponse:
        """Request ethics review for an action"""
        self.total_reviews += 1
        
        try:
            # Generate request ID if not provided
            if not request.request_id:
                request.request_id = str(uuid.uuid4())
            
            # Set timestamp
            if not request.timestamp:
                request.timestamp = datetime.utcnow().isoformat()
            
            # Check cache first
            cache_key = self._generate_cache_key(request)
            cached_response = await self._get_cached_response(cache_key)
            if cached_response and not self._is_expired(cached_response):
                self.logger.debug(f"Returning cached ethics response for {request.request_id}")
                return cached_response
            
            # Perform ethics analysis
            response = await self._analyze_ethics_request(request)
            
            # Cache the response
            await self._cache_response(cache_key, response)
            
            # Log the decision
            await self._log_ethics_decision(request, response)
            
            # Update metrics
            if response.human_review_required:
                self.human_reviews += 1
                await self._queue_for_human_review(request)
            else:
                self.auto_approved += 1
            
            if not response.approved:
                self.compliance_violations += 1
            
            self.logger.info(f"Ethics review completed for {request.request_id}: {response.status.value}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Ethics review failed for {request.request_id}: {e}")
            
            # Return conservative response on error
            return EthicsResponse(
                request_id=request.request_id,
                status=ReviewStatus.REJECTED,
                approved=False,
                confidence=0.0,
                rationale=f"Ethics review failed: {str(e)}",
                recommendations=["Manual review required", "Contact compliance team"],
                compliance_status={framework: False for framework in request.compliance_requirements},
                risk_score=1.0,
                human_review_required=True,
                metadata={"error": str(e)}
            )
    
    async def _analyze_ethics_request(self, request: EthicsRequest) -> EthicsResponse:
        """Analyze ethics request and generate response"""
        # Calculate risk score
        risk_score = await self._calculate_risk_score(request)
        
        # Check compliance requirements
        compliance_status = await self._check_compliance(request)
        
        # Determine if human review is required
        human_review_required = await self._requires_human_review(request, risk_score, compliance_status)
        
        # Generate rationale and recommendations
        rationale, recommendations = await self._generate_rationale_and_recommendations(request, risk_score, compliance_status)
        
        # Determine approval status
        approved = await self._determine_approval(request, risk_score, compliance_status, human_review_required)
        
        # Calculate confidence
        confidence = await self._calculate_confidence(request, risk_score, compliance_status)
        
        # Determine review status
        if human_review_required:
            status = ReviewStatus.ESCALATED
        elif approved:
            status = ReviewStatus.APPROVED
        else:
            status = ReviewStatus.REJECTED
        
        # Set expiry time for approved decisions
        expiry_time = None
        if approved and not human_review_required:
            expiry_time = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        
        return EthicsResponse(
            request_id=request.request_id,
            status=status,
            approved=approved,
            confidence=confidence,
            rationale=rationale,
            recommendations=recommendations,
            compliance_status=compliance_status,
            risk_score=risk_score,
            human_review_required=human_review_required,
            expiry_time=expiry_time,
            metadata={
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "risk_factors": request.risk_factors,
                "priority": request.priority.value
            }
        )
    
    async def _calculate_risk_score(self, request: EthicsRequest) -> float:
        """Calculate risk score for the request"""
        risk_score = 0.0
        
        # Base risk by action type
        action_risk = {
            ActionType.CONVERSATION: 0.1,
            ActionType.PHONE_CALL: 0.3,
            ActionType.DATA_ACCESS: 0.5,
            ActionType.DECISION_MAKING: 0.4,
            ActionType.AUTOMATION: 0.6,
            ActionType.ESCALATION: 0.2
        }
        risk_score += action_risk.get(request.action_type, 0.3)
        
        # Risk factors analysis
        for factor in request.risk_factors:
            if "pii" in factor.lower() or "personal" in factor.lower():
                risk_score += self.risk_weights["pii_exposure"]
            elif "financial" in factor.lower() or "payment" in factor.lower():
                risk_score += self.risk_weights["financial_impact"]
            elif "regulatory" in factor.lower() or "compliance" in factor.lower():
                risk_score += self.risk_weights["regulatory_risk"]
            elif "reputation" in factor.lower() or "brand" in factor.lower():
                risk_score += self.risk_weights["reputation_risk"]
            else:
                risk_score += self.risk_weights["operational_risk"]
        
        # Priority adjustment
        priority_multiplier = {
            EthicsLevel.LOW: 0.5,
            EthicsLevel.MEDIUM: 1.0,
            EthicsLevel.HIGH: 1.5,
            EthicsLevel.CRITICAL: 2.0
        }
        risk_score *= priority_multiplier[request.priority]
        
        # Content analysis (simplified)
        content_lower = request.content.lower()
        sensitive_keywords = ["password", "ssn", "credit card", "bank account", "medical", "health", "diagnosis"]
        for keyword in sensitive_keywords:
            if keyword in content_lower:
                risk_score += 0.1
        
        # Normalize to 0-1 range
        return min(risk_score, 1.0)
    
    async def _check_compliance(self, request: EthicsRequest) -> Dict[ComplianceFramework, bool]:
        """Check compliance against required frameworks"""
        compliance_status = {}
        
        for framework in request.compliance_requirements:
            compliance_status[framework] = await self._check_framework_compliance(request, framework)
        
        return compliance_status
    
    async def _check_framework_compliance(self, request: EthicsRequest, framework: ComplianceFramework) -> bool:
        """Check compliance against specific framework"""
        # Get relevant rules for this framework
        relevant_rules = [rule for rule in self.compliance_rules.values() 
                         if rule.framework == framework and rule.enabled]
        
        for rule in relevant_rules:
            if not await self._evaluate_rule(request, rule):
                return False
        
        return True
    
    async def _evaluate_rule(self, request: EthicsRequest, rule: ComplianceRule) -> bool:
        """Evaluate a specific compliance rule"""
        # Simplified rule evaluation logic
        # In production, this would be more sophisticated
        
        conditions = rule.conditions
        context = request.context
        content = request.content.lower()
        
        # GDPR consent check
        if rule.rule_id == "gdpr_consent":
            if conditions.get("requires_consent") and conditions.get("data_processing"):
                return context.get("user_consent", False)
        
        # TCPA consent check
        elif rule.rule_id == "tcpa_consent":
            if conditions.get("automated_call") and request.action_type == ActionType.PHONE_CALL:
                return context.get("call_consent", False) and not context.get("dnc_listed", False)
        
        # HIPAA PHI check
        elif rule.rule_id == "hipaa_phi":
            if conditions.get("health_data"):
                health_keywords = ["medical", "health", "diagnosis", "treatment", "prescription"]
                has_health_data = any(keyword in content for keyword in health_keywords)
                if has_health_data:
                    return context.get("hipaa_compliant", False)
        
        # PCI DSS card data check
        elif rule.rule_id == "pci_card_data":
            if conditions.get("payment_data"):
                payment_keywords = ["credit card", "card number", "cvv", "payment"]
                has_payment_data = any(keyword in content for keyword in payment_keywords)
                if has_payment_data:
                    return context.get("pci_compliant", False)
        
        return True
    
    async def _requires_human_review(self, request: EthicsRequest, risk_score: float, compliance_status: Dict[ComplianceFramework, bool]) -> bool:
        """Determine if human review is required"""
        # High risk score requires human review
        if risk_score > 0.7:
            return True
        
        # Critical priority requires human review
        if request.priority == EthicsLevel.CRITICAL:
            return True
        
        # Any compliance failure requires human review
        if not all(compliance_status.values()):
            return True
        
        # Specific action types require human review
        if request.action_type in [ActionType.DECISION_MAKING, ActionType.AUTOMATION]:
            return True
        
        # Context-based requirements
        if request.context.get("requires_human_review", False):
            return True
        
        return False
    
    async def _generate_rationale_and_recommendations(self, request: EthicsRequest, risk_score: float, compliance_status: Dict[ComplianceFramework, bool]) -> Tuple[str, List[str]]:
        """Generate rationale and recommendations"""
        rationale_parts = []
        recommendations = []
        
        # Risk assessment rationale
        if risk_score < 0.3:
            rationale_parts.append("Low risk assessment based on action type and content analysis.")
        elif risk_score < 0.7:
            rationale_parts.append("Medium risk assessment requires careful monitoring.")
        else:
            rationale_parts.append("High risk assessment requires immediate attention.")
            recommendations.append("Implement additional safeguards")
            recommendations.append("Monitor closely for compliance")
        
        # Compliance rationale
        failed_frameworks = [framework.value for framework, status in compliance_status.items() if not status]
        if failed_frameworks:
            rationale_parts.append(f"Compliance violations detected: {', '.join(failed_frameworks)}")
            recommendations.append("Address compliance violations before proceeding")
            recommendations.append("Consult legal team if necessary")
        else:
            rationale_parts.append("All required compliance frameworks satisfied.")
        
        # Action-specific recommendations
        if request.action_type == ActionType.PHONE_CALL:
            recommendations.append("Verify TCPA compliance and consent")
            recommendations.append("Maintain call recordings for audit")
        elif request.action_type == ActionType.DATA_ACCESS:
            recommendations.append("Log all data access for audit trail")
            recommendations.append("Implement principle of least privilege")
        
        # Priority-based recommendations
        if request.priority == EthicsLevel.CRITICAL:
            recommendations.append("Escalate to senior management")
            recommendations.append("Document decision rationale thoroughly")
        
        rationale = " ".join(rationale_parts)
        
        return rationale, recommendations
    
    async def _determine_approval(self, request: EthicsRequest, risk_score: float, compliance_status: Dict[ComplianceFramework, bool], human_review_required: bool) -> bool:
        """Determine if the request should be approved"""
        # Reject if any compliance framework fails
        if not all(compliance_status.values()):
            return False
        
        # Reject if risk score is too high for auto-approval
        if risk_score > 0.8:
            return False
        
        # Approve low-risk requests that pass compliance
        if risk_score < 0.3 and not human_review_required:
            return True
        
        # Medium risk requires human review but can be conditionally approved
        if risk_score < 0.7 and human_review_required:
            return False  # Wait for human review
        
        # Default to approval for compliant, low-risk requests
        return True
    
    async def _calculate_confidence(self, request: EthicsRequest, risk_score: float, compliance_status: Dict[ComplianceFramework, bool]) -> float:
        """Calculate confidence in the ethics decision"""
        confidence = 0.8  # Base confidence
        
        # Adjust based on risk score clarity
        if risk_score < 0.2 or risk_score > 0.8:
            confidence += 0.1  # Clear high or low risk
        else:
            confidence -= 0.1  # Ambiguous risk level
        
        # Adjust based on compliance clarity
        if all(compliance_status.values()) or not any(compliance_status.values()):
            confidence += 0.1  # Clear compliance status
        else:
            confidence -= 0.2  # Mixed compliance status
        
        # Adjust based on available context
        context_completeness = len(request.context) / 10  # Assume 10 is ideal
        confidence += min(context_completeness * 0.1, 0.1)
        
        return min(max(confidence, 0.0), 1.0)
    
    def _generate_cache_key(self, request: EthicsRequest) -> str:
        """Generate cache key for ethics request"""
        # Create hash of relevant request components
        key_components = {
            "action_type": request.action_type.value,
            "content_hash": hashlib.md5(request.content.encode()).hexdigest(),
            "risk_factors": sorted(request.risk_factors),
            "compliance_requirements": sorted([f.value for f in request.compliance_requirements]),
            "priority": request.priority.value
        }
        
        key_string = json.dumps(key_components, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    async def _get_cached_response(self, cache_key: str) -> Optional[EthicsResponse]:
        """Get cached ethics response"""
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(f"ethics:{cache_key}")
                if cached_data:
                    response_dict = json.loads(cached_data)
                    # Convert back to EthicsResponse object
                    response_dict['status'] = ReviewStatus(response_dict['status'])
                    response_dict['compliance_status'] = {
                        ComplianceFramework(k): v for k, v in response_dict['compliance_status'].items()
                    }
                    return EthicsResponse(**response_dict)
            except Exception as e:
                self.logger.warning(f"Cache retrieval failed: {e}")
        
        return self.ethics_cache.get(cache_key)
    
    async def _cache_response(self, cache_key: str, response: EthicsResponse):
        """Cache ethics response"""
        # Cache in memory
        self.ethics_cache[cache_key] = response
        
        # Cache in Redis if available
        if self.redis_client:
            try:
                response_dict = asdict(response)
                response_dict['status'] = response.status.value
                response_dict['compliance_status'] = {
                    k.value: v for k, v in response.compliance_status.items()
                }
                
                await self.redis_client.setex(
                    f"ethics:{cache_key}",
                    3600,  # 1 hour TTL
                    json.dumps(response_dict)
                )
            except Exception as e:
                self.logger.warning(f"Cache storage failed: {e}")
    
    def _is_expired(self, response: EthicsResponse) -> bool:
        """Check if cached response is expired"""
        if not response.expiry_time:
            return False
        
        expiry = datetime.fromisoformat(response.expiry_time)
        return datetime.utcnow() > expiry
    
    async def _log_ethics_decision(self, request: EthicsRequest, response: EthicsResponse):
        """Log ethics decision for audit"""
        audit_log = AuditLog(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            agent_id=request.agent_id,
            action_type=request.action_type,
            request_id=request.request_id,
            decision=response.status.value,
            rationale=response.rationale,
            compliance_frameworks=request.compliance_requirements,
            risk_score=response.risk_score,
            human_reviewer=response.reviewer_id,
            metadata={
                "confidence": response.confidence,
                "human_review_required": response.human_review_required,
                "recommendations": response.recommendations
            }
        )
        
        self.audit_logs.append(audit_log)
        
        # In production, this would be stored in a secure audit database
        self.logger.info(f"Ethics decision logged: {audit_log.log_id}")
    
    async def _queue_for_human_review(self, request: EthicsRequest):
        """Queue request for human review"""
        self.human_review_queue.append(request)
        self.logger.info(f"Request {request.request_id} queued for human review")
    
    async def get_human_review_queue(self) -> List[EthicsRequest]:
        """Get pending human review requests"""
        return self.human_review_queue.copy()
    
    async def process_human_review(self, request_id: str, reviewer_id: str, approved: bool, rationale: str) -> EthicsResponse:
        """Process human review decision"""
        # Find the request in queue
        request = None
        for i, req in enumerate(self.human_review_queue):
            if req.request_id == request_id:
                request = self.human_review_queue.pop(i)
                break
        
        if not request:
            raise ValueError(f"Request {request_id} not found in human review queue")
        
        # Create response based on human decision
        response = EthicsResponse(
            request_id=request_id,
            status=ReviewStatus.APPROVED if approved else ReviewStatus.REJECTED,
            approved=approved,
            confidence=1.0,  # Human review has high confidence
            rationale=rationale,
            recommendations=[],
            compliance_status={framework: approved for framework in request.compliance_requirements},
            risk_score=0.0 if approved else 1.0,
            human_review_required=False,
            reviewer_id=reviewer_id,
            metadata={
                "human_reviewed": True,
                "review_timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Log the human decision
        await self._log_ethics_decision(request, response)
        
        self.logger.info(f"Human review completed for {request_id} by {reviewer_id}: {approved}")
        
        return response
    
    async def get_audit_logs(self, start_date: Optional[str] = None, end_date: Optional[str] = None, agent_id: Optional[str] = None) -> List[AuditLog]:
        """Get audit logs with optional filtering"""
        filtered_logs = self.audit_logs.copy()
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log.timestamp) >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log.timestamp) <= end_dt]
        
        if agent_id:
            filtered_logs = [log for log in filtered_logs if log.agent_id == agent_id]
        
        return filtered_logs
    
    async def get_compliance_report(self) -> Dict[str, Any]:
        """Generate compliance report"""
        total_logs = len(self.audit_logs)
        if total_logs == 0:
            return {"message": "No audit data available"}
        
        # Calculate compliance metrics
        approved_count = len([log for log in self.audit_logs if log.decision == "approved"])
        rejected_count = len([log for log in self.audit_logs if log.decision == "rejected"])
        escalated_count = len([log for log in self.audit_logs if log.decision == "escalated"])
        
        # Framework-specific metrics
        framework_metrics = {}
        for framework in ComplianceFramework:
            framework_logs = [log for log in self.audit_logs if framework in log.compliance_frameworks]
            framework_metrics[framework.value] = {
                "total_requests": len(framework_logs),
                "compliance_rate": len([log for log in framework_logs if log.decision == "approved"]) / len(framework_logs) if framework_logs else 0
            }
        
        # Risk distribution
        risk_distribution = {
            "low": len([log for log in self.audit_logs if log.risk_score < 0.3]),
            "medium": len([log for log in self.audit_logs if 0.3 <= log.risk_score < 0.7]),
            "high": len([log for log in self.audit_logs if log.risk_score >= 0.7])
        }
        
        return {
            "report_generated": datetime.utcnow().isoformat(),
            "total_reviews": total_logs,
            "approval_rate": approved_count / total_logs,
            "rejection_rate": rejected_count / total_logs,
            "escalation_rate": escalated_count / total_logs,
            "human_review_rate": self.human_reviews / self.total_reviews if self.total_reviews > 0 else 0,
            "framework_compliance": framework_metrics,
            "risk_distribution": risk_distribution,
            "performance_metrics": {
                "total_reviews": self.total_reviews,
                "auto_approved": self.auto_approved,
                "human_reviews": self.human_reviews,
                "compliance_violations": self.compliance_violations
            }
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics"""
        return {
            "total_reviews": self.total_reviews,
            "auto_approved": self.auto_approved,
            "human_reviews": self.human_reviews,
            "compliance_violations": self.compliance_violations,
            "pending_human_reviews": len(self.human_review_queue),
            "cached_responses": len(self.ethics_cache),
            "audit_logs_count": len(self.audit_logs),
            "compliance_rules_count": len(self.compliance_rules),
            "service_status": {
                "redis_available": self.redis_client is not None,
                "audit_logging_active": True,
                "compliance_rules_loaded": len(self.compliance_rules) > 0
            }
        }
    
    async def close(self):
        """Close service and cleanup resources"""
        self.logger.info("Closing QHC Governance Service")
        
        # Close Redis connection
        if self.redis_client:
            await self.redis_client.close()
        
        # Clear caches
        self.ethics_cache.clear()
        self.human_review_queue.clear()
        
        self.logger.info("QHC Governance Service closed")

# Example usage and testing
if __name__ == "__main__":
    async def test_qhc_governance():
        """Test the QHC Governance service"""
        config = {
            "redis_url": "redis://localhost:6379"
        }
        
        service = QHCGovernance(config)
        await service.initialize()
        
        # Test ethics requests
        test_requests = [
            EthicsRequest(
                request_id="test_1",
                agent_id="chat_agent_1",
                action_type=ActionType.CONVERSATION,
                content="Hello, can you help me with my account balance?",
                context={"user_consent": True, "authenticated": True},
                risk_factors=["financial_data"],
                compliance_requirements=[ComplianceFramework.GDPR],
                priority=EthicsLevel.LOW
            ),
            EthicsRequest(
                request_id="test_2",
                agent_id="calling_agent_1",
                action_type=ActionType.PHONE_CALL,
                content="Automated call to discuss loan options",
                context={"call_consent": False, "dnc_listed": True},
                risk_factors=["automated_call", "financial_product"],
                compliance_requirements=[ComplianceFramework.TCPA],
                priority=EthicsLevel.HIGH
            ),
            EthicsRequest(
                request_id="test_3",
                agent_id="data_agent_1",
                action_type=ActionType.DATA_ACCESS,
                content="Accessing patient medical records for analysis",
                context={"hipaa_compliant": True, "authorized_access": True},
                risk_factors=["health_data", "pii_exposure"],
                compliance_requirements=[ComplianceFramework.HIPAA, ComplianceFramework.GDPR],
                priority=EthicsLevel.CRITICAL
            )
        ]
        
        for i, request in enumerate(test_requests):
            print(f"\n--- Test {i+1}: {request.action_type.value} ---")
            try:
                response = await service.request_ethics_review(request)
                print(f"Status: {response.status.value}")
                print(f"Approved: {response.approved}")
                print(f"Confidence: {response.confidence:.2f}")
                print(f"Risk Score: {response.risk_score:.2f}")
                print(f"Human Review Required: {response.human_review_required}")
                print(f"Rationale: {response.rationale}")
                print(f"Recommendations: {response.recommendations}")
                print(f"Compliance Status: {response.compliance_status}")
            except Exception as e:
                print(f"Error: {e}")
        
        # Get metrics
        metrics = await service.get_metrics()
        print(f"\n--- Service Metrics ---")
        print(json.dumps(metrics, indent=2))
        
        # Get compliance report
        report = await service.get_compliance_report()
        print(f"\n--- Compliance Report ---")
        print(json.dumps(report, indent=2))
        
        await service.close()
    
    # Run test
    asyncio.run(test_qhc_governance())