"""
Compliance Manager for NQBA Ecosystem
Handles SOC 2, GDPR/CCPA, and SFG insurance compliance
"""

import os
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""

    SOC2_TYPE1 = "soc2_type1"
    SOC2_TYPE2 = "soc2_type2"
    GDPR = "gdpr"
    CCPA = "ccpa"
    SFG_INSURANCE = "sfg_insurance"


class ControlCategory(Enum):
    """SOC 2 control categories"""

    CC = "CC"  # Common Criteria
    AIC = "AIC"  # Availability, Integrity, Confidentiality


class DataSubjectType(Enum):
    """GDPR/CCPA data subject types"""

    INDIVIDUAL = "individual"
    BUSINESS = "business"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"
    PROSPECT = "prospect"


class DataProcessingPurpose(Enum):
    """Data processing purposes"""

    SERVICE_PROVISION = "service_provision"
    MARKETING = "marketing"
    ANALYTICS = "analytics"
    COMPLIANCE = "compliance"
    LEGAL_OBLIGATION = "legal_obligation"
    LEGITIMATE_INTEREST = "legitimate_interest"


@dataclass
class SOC2Control:
    """SOC 2 control definition"""

    control_id: str
    category: ControlCategory
    name: str
    description: str
    requirements: List[str] = field(default_factory=list)
    test_procedures: List[str] = field(default_factory=list)
    evidence_requirements: List[str] = field(default_factory=list)
    is_implemented: bool = False
    last_assessed: Optional[datetime] = None
    next_assessment: Optional[datetime] = None
    risk_level: str = "medium"


@dataclass
class DataFlow:
    """Data flow mapping for GDPR/CCPA"""

    flow_id: str
    name: str
    description: str
    data_subjects: List[DataSubjectType] = field(default_factory=list)
    data_categories: List[str] = field(default_factory=list)
    purposes: List[DataProcessingPurpose] = field(default_factory=list)
    third_parties: List[str] = field(default_factory=list)
    retention_period_days: int = 0
    legal_basis: str = ""
    consent_required: bool = False
    data_minimization: bool = True
    encryption_at_rest: bool = True
    encryption_in_transit: bool = True
    access_controls: bool = True
    audit_logging: bool = True


@dataclass
class ConsentRecord:
    """GDPR/CCPA consent record"""

    consent_id: str
    data_subject_id: str
    data_subject_type: DataSubjectType
    purpose: DataProcessingPurpose
    consent_given: bool
    consent_timestamp: datetime
    consent_method: str
    consent_version: str
    legal_basis: str
    withdrawal_timestamp: Optional[datetime] = None
    data_categories: List[str] = field(default_factory=list)
    third_parties: List[str] = field(default_factory=list)


@dataclass
class SFGCompliance:
    """SFG insurance compliance requirements"""

    compliance_id: str
    requirement: str
    description: str
    state_requirements: Dict[str, List[str]] = field(default_factory=dict)
    compliance_status: str = "pending"
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    documentation_required: List[str] = field(default_factory=list)
    risk_assessment: str = "medium"


class ComplianceManager:
    """
    Comprehensive compliance manager for regulatory requirements
    Handles SOC 2, GDPR/CCPA, and SFG insurance compliance
    """

    def __init__(self):
        self.soc2_controls: Dict[str, SOC2Control] = {}
        self.data_flows: Dict[str, DataFlow] = {}
        self.consent_records: Dict[str, ConsentRecord] = {}
        self.sfg_compliance: Dict[str, SFGCompliance] = {}
        self._initialize_soc2_controls()
        self._initialize_data_flows()
        self._initialize_sfg_compliance()
        self._start_compliance_monitoring()

    def _initialize_soc2_controls(self):
        """Initialize SOC 2 Type 2 controls"""
        controls = [
            # Common Criteria (CC) Controls
            SOC2Control(
                control_id="CC1.1",
                category=ControlCategory.CC,
                name="Control Environment",
                description="The entity demonstrates a commitment to integrity and ethical values",
                requirements=[
                    "Establish and maintain a control environment",
                    "Demonstrate commitment to integrity and ethical values",
                    "Exercise oversight responsibility",
                    "Demonstrate commitment to competence",
                    "Enforce accountability",
                ],
                test_procedures=[
                    "Review control environment documentation",
                    "Interview management about control environment",
                    "Observe control environment in operation",
                ],
                evidence_requirements=[
                    "Control environment policies and procedures",
                    "Management communications",
                    "Organizational structure documentation",
                ],
            ),
            SOC2Control(
                control_id="CC2.1",
                category=ControlCategory.CC,
                name="Communication and Information",
                description="The entity communicates information to support the functioning of internal control",
                requirements=[
                    "Identify and communicate information requirements",
                    "Communicate information to support internal control",
                    "Communicate information to support external reporting",
                ],
                test_procedures=[
                    "Review communication policies and procedures",
                    "Interview personnel about communication processes",
                    "Review communication documentation",
                ],
                evidence_requirements=[
                    "Communication policies and procedures",
                    "Communication logs and records",
                    "Training materials",
                ],
            ),
            SOC2Control(
                control_id="CC3.1",
                category=ControlCategory.CC,
                name="Risk Assessment",
                description="The entity identifies and assesses risks that could affect the achievement of objectives",
                requirements=[
                    "Identify risks to achievement of objectives",
                    "Assess identified risks",
                    "Consider potential for fraud",
                    "Identify and assess changes that could affect internal control",
                ],
                test_procedures=[
                    "Review risk assessment documentation",
                    "Interview personnel about risk assessment process",
                    "Review risk assessment results",
                ],
                evidence_requirements=[
                    "Risk assessment policies and procedures",
                    "Risk assessment documentation",
                    "Risk register",
                ],
            ),
            SOC2Control(
                control_id="CC4.1",
                category=ControlCategory.CC,
                name="Control Activities",
                description="The entity selects and develops control activities that contribute to the mitigation of risks",
                requirements=[
                    "Select and develop control activities",
                    "Select and develop general control activities",
                    "Select and develop technology control activities",
                ],
                test_procedures=[
                    "Review control activities documentation",
                    "Observe control activities in operation",
                    "Test control activities effectiveness",
                ],
                evidence_requirements=[
                    "Control activities policies and procedures",
                    "Control activities documentation",
                    "Control testing results",
                ],
            ),
            SOC2Control(
                control_id="CC5.1",
                category=ControlCategory.CC,
                name="Monitoring Activities",
                description="The entity selects, develops, and performs ongoing and/or separate evaluations",
                requirements=[
                    "Select, develop, and perform ongoing evaluations",
                    "Select, develop, and perform separate evaluations",
                    "Evaluate and communicate deficiencies",
                ],
                test_procedures=[
                    "Review monitoring activities documentation",
                    "Interview personnel about monitoring process",
                    "Review monitoring results",
                ],
                evidence_requirements=[
                    "Monitoring policies and procedures",
                    "Monitoring documentation",
                    "Monitoring results and reports",
                ],
            ),
        ]

        for control in controls:
            self.soc2_controls[control.control_id] = control

    def _initialize_data_flows(self):
        """Initialize GDPR/CCPA data flow mappings"""
        flows = [
            DataFlow(
                flow_id="user_registration",
                name="User Registration and Onboarding",
                description="Data collected during user registration and onboarding process",
                data_subjects=[DataSubjectType.INDIVIDUAL, DataSubjectType.BUSINESS],
                data_categories=[
                    "personal_identifiers",
                    "contact_information",
                    "business_information",
                ],
                purposes=[
                    DataProcessingPurpose.SERVICE_PROVISION,
                    DataProcessingPurpose.COMPLIANCE,
                ],
                third_parties=["identity_verification_service"],
                retention_period_days=2555,  # 7 years for compliance
                legal_basis="contract_performance",
                consent_required=True,
            ),
            DataFlow(
                flow_id="quantum_optimization",
                name="Quantum Optimization Services",
                description="Data processed during quantum optimization operations",
                data_subjects=[DataSubjectType.CUSTOMER, DataSubjectType.BUSINESS],
                data_categories=["business_data", "optimization_parameters", "results"],
                purposes=[
                    DataProcessingPurpose.SERVICE_PROVISION,
                    DataProcessingPurpose.ANALYTICS,
                ],
                third_parties=["dynex_quantum_platform"],
                retention_period_days=1095,  # 3 years for business purposes
                legal_basis="legitimate_interest",
                consent_required=False,
            ),
            DataFlow(
                flow_id="marketing_communications",
                name="Marketing and Communications",
                description="Data used for marketing communications and lead generation",
                data_subjects=[DataSubjectType.PROSPECT, DataSubjectType.CUSTOMER],
                data_categories=[
                    "contact_information",
                    "preferences",
                    "interaction_history",
                ],
                purposes=[
                    DataProcessingPurpose.MARKETING,
                    DataProcessingPurpose.ANALYTICS,
                ],
                third_parties=["email_service_provider", "analytics_platform"],
                retention_period_days=730,  # 2 years for marketing
                legal_basis="consent",
                consent_required=True,
            ),
        ]

        for flow in flows:
            self.data_flows[flow.flow_id] = flow

    def _initialize_sfg_compliance(self):
        """Initialize SFG insurance compliance requirements"""
        compliance_items = [
            SFGCompliance(
                compliance_id="sfg_001",
                requirement="State Licensing Requirements",
                description="Compliance with state-specific insurance licensing requirements",
                state_requirements={
                    "CA": ["Insurance license", "Bond requirement", "E&O insurance"],
                    "NY": [
                        "Insurance license",
                        "Financial statements",
                        "Character references",
                    ],
                    "TX": ["Insurance license", "Surety bond", "Continuing education"],
                },
                documentation_required=[
                    "State license applications",
                    "Financial statements",
                    "Character references",
                    "Continuing education certificates",
                ],
            ),
            SFGCompliance(
                compliance_id="sfg_002",
                requirement="Disclosure Requirements",
                description="Required disclosures to clients and regulatory bodies",
                state_requirements={
                    "CA": [
                        "Fee disclosure",
                        "Conflict of interest",
                        "Compensation structure",
                    ],
                    "NY": [
                        "Fee disclosure",
                        "Material relationships",
                        "Regulatory status",
                    ],
                    "TX": [
                        "Fee disclosure",
                        "Business relationships",
                        "Regulatory compliance",
                    ],
                },
                documentation_required=[
                    "Disclosure forms",
                    "Client agreements",
                    "Regulatory filings",
                ],
            ),
            SFGCompliance(
                compliance_id="sfg_003",
                requirement="Data Privacy and Security",
                description="Compliance with state data privacy and security requirements",
                state_requirements={
                    "CA": [
                        "CCPA compliance",
                        "Data security measures",
                        "Breach notification",
                    ],
                    "NY": [
                        "NYDFS cybersecurity",
                        "Data protection",
                        "Incident response",
                    ],
                    "TX": [
                        "Data breach notification",
                        "Security measures",
                        "Privacy policies",
                    ],
                },
                documentation_required=[
                    "Privacy policies",
                    "Security assessments",
                    "Incident response plans",
                    "Data processing agreements",
                ],
            ),
        ]

        for item in compliance_items:
            self.sfg_compliance[item.compliance_id] = item

    def assess_soc2_control(
        self, control_id: str, assessment_data: Dict[str, Any]
    ) -> bool:
        """Assess a SOC 2 control and update implementation status"""
        if control_id not in self.soc2_controls:
            return False

        control = self.soc2_controls[control_id]

        # Update control assessment
        control.is_implemented = assessment_data.get("is_implemented", False)
        control.last_assessed = datetime.now(timezone.utc)
        control.next_assessment = datetime.now(timezone.utc) + timedelta(days=90)
        control.risk_level = assessment_data.get("risk_level", "medium")

        logger.info(f"Assessed SOC 2 control {control_id}: {control.is_implemented}")
        return True

    def get_soc2_status(self) -> Dict[str, Any]:
        """Get overall SOC 2 compliance status"""
        total_controls = len(self.soc2_controls)
        implemented_controls = sum(
            1 for control in self.soc2_controls.values() if control.is_implemented
        )
        pending_assessments = sum(
            1
            for control in self.soc2_controls.values()
            if control.next_assessment
            and control.next_assessment < datetime.now(timezone.utc)
        )

        # Group by category
        category_status = {}
        for control in self.soc2_controls.values():
            category = control.category.value
            if category not in category_status:
                category_status[category] = {"total": 0, "implemented": 0}

            category_status[category]["total"] += 1
            if control.is_implemented:
                category_status[category]["implemented"] += 1

        return {
            "total_controls": total_controls,
            "implemented_controls": implemented_controls,
            "compliance_percentage": (
                (implemented_controls / total_controls * 100)
                if total_controls > 0
                else 0
            ),
            "pending_assessments": pending_assessments,
            "category_status": category_status,
            "next_assessment": min(
                [
                    c.next_assessment
                    for c in self.soc2_controls.values()
                    if c.next_assessment
                ],
                default=None,
            ),
        }

    def record_consent(
        self,
        data_subject_id: str,
        data_subject_type: DataSubjectType,
        purpose: DataProcessingPurpose,
        consent_given: bool,
        consent_method: str,
        legal_basis: str,
        data_categories: List[str],
        third_parties: List[str],
    ) -> str:
        """Record GDPR/CCPA consent"""
        consent_id = f"consent_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        consent_record = ConsentRecord(
            consent_id=consent_id,
            data_subject_id=data_subject_id,
            data_subject_type=data_subject_type,
            purpose=purpose,
            consent_given=consent_given,
            consent_timestamp=datetime.now(timezone.utc),
            consent_method=consent_method,
            consent_version="1.0",
            legal_basis=legal_basis,
            data_categories=data_categories,
            third_parties=third_parties,
        )

        self.consent_records[consent_id] = consent_record

        logger.info(f"Recorded consent {consent_id} for {data_subject_id}")
        return consent_id

    def withdraw_consent(self, consent_id: str) -> bool:
        """Withdraw GDPR/CCPA consent"""
        if consent_id not in self.consent_records:
            return False

        consent = self.consent_records[consent_id]
        consent.withdrawal_timestamp = datetime.now(timezone.utc)

        logger.info(f"Withdrew consent {consent_id}")
        return True

    def get_consent_status(self, data_subject_id: str) -> Dict[str, Any]:
        """Get consent status for a data subject"""
        active_consents = []
        withdrawn_consents = []

        for consent in self.consent_records.values():
            if consent.data_subject_id == data_subject_id:
                if consent.withdrawal_timestamp:
                    withdrawn_consents.append(
                        {
                            "consent_id": consent.consent_id,
                            "purpose": consent.purpose.value,
                            "consent_timestamp": consent.consent_timestamp.isoformat(),
                            "withdrawal_timestamp": consent.withdrawal_timestamp.isoformat(),
                            "legal_basis": consent.legal_basis,
                        }
                    )
                else:
                    active_consents.append(
                        {
                            "consent_id": consent.consent_id,
                            "purpose": consent.purpose.value,
                            "consent_timestamp": consent.consent_timestamp.isoformat(),
                            "legal_basis": consent.legal_basis,
                            "data_categories": consent.data_categories,
                            "third_parties": consent.third_parties,
                        }
                    )

        return {
            "data_subject_id": data_subject_id,
            "active_consents": active_consents,
            "withdrawn_consents": withdrawn_consents,
            "total_consents": len(active_consents) + len(withdrawn_consents),
        }

    def assess_data_flow_compliance(self, flow_id: str) -> Dict[str, Any]:
        """Assess GDPR/CCPA compliance for a data flow"""
        if flow_id not in self.data_flows:
            return {}

        flow = self.data_flows[flow_id]

        # Check compliance requirements
        compliance_checks = {
            "data_minimization": flow.data_minimization,
            "encryption_at_rest": flow.encryption_at_rest,
            "encryption_in_transit": flow.encryption_in_transit,
            "access_controls": flow.access_controls,
            "audit_logging": flow.audit_logging,
            "consent_management": flow.consent_required,
            "retention_policy": flow.retention_period_days > 0,
            "third_party_assessment": len(flow.third_parties) > 0,
        }

        compliance_score = (
            sum(compliance_checks.values()) / len(compliance_checks) * 100
        )

        return {
            "flow_id": flow_id,
            "flow_name": flow.name,
            "compliance_score": compliance_score,
            "compliance_checks": compliance_checks,
            "data_categories": flow.data_categories,
            "purposes": [p.value for p in flow.purposes],
            "retention_period_days": flow.retention_period_days,
            "legal_basis": flow.legal_basis,
        }

    def get_gdpr_ccpa_status(self) -> Dict[str, Any]:
        """Get overall GDPR/CCPA compliance status"""
        total_flows = len(self.data_flows)
        compliance_scores = []

        for flow_id in self.data_flows.keys():
            compliance = self.assess_data_flow_compliance(flow_id)
            if compliance:
                compliance_scores.append(compliance["compliance_score"])

        avg_compliance = (
            sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0
        )

        # Count consent records
        total_consents = len(self.consent_records)
        active_consents = sum(
            1 for c in self.consent_records.values() if not c.withdrawal_timestamp
        )
        withdrawn_consents = total_consents - active_consents

        return {
            "total_data_flows": total_flows,
            "average_compliance_score": avg_compliance,
            "total_consents": total_consents,
            "active_consents": active_consents,
            "withdrawn_consents": withdrawn_consents,
            "data_flows": [
                self.assess_data_flow_compliance(flow_id)
                for flow_id in self.data_flows.keys()
            ],
        }

    def assess_sfg_compliance(
        self, compliance_id: str, assessment_data: Dict[str, Any]
    ) -> bool:
        """Assess SFG insurance compliance requirement"""
        if compliance_id not in self.sfg_compliance:
            return False

        compliance = self.sfg_compliance[compliance_id]

        # Update compliance status
        compliance.compliance_status = assessment_data.get("status", "pending")
        compliance.last_reviewed = datetime.now(timezone.utc)
        compliance.next_review = datetime.now(timezone.utc) + timedelta(days=30)
        compliance.risk_assessment = assessment_data.get("risk_assessment", "medium")

        logger.info(
            f"Assessed SFG compliance {compliance_id}: {compliance.compliance_status}"
        )
        return True

    def get_sfg_compliance_status(self) -> Dict[str, Any]:
        """Get overall SFG insurance compliance status"""
        total_requirements = len(self.sfg_compliance)
        compliant_requirements = sum(
            1
            for c in self.sfg_compliance.values()
            if c.compliance_status == "compliant"
        )
        pending_reviews = sum(
            1
            for c in self.sfg_compliance.values()
            if c.next_review and c.next_review < datetime.now(timezone.utc)
        )

        # Group by state
        state_compliance = {}
        for compliance in self.sfg_compliance.values():
            for state in compliance.state_requirements.keys():
                if state not in state_compliance:
                    state_compliance[state] = {"total": 0, "compliant": 0}

                state_compliance[state]["total"] += 1
                if compliance.compliance_status == "compliant":
                    state_compliance[state]["compliant"] += 1

        return {
            "total_requirements": total_requirements,
            "compliant_requirements": compliant_requirements,
            "compliance_percentage": (
                (compliant_requirements / total_requirements * 100)
                if total_requirements > 0
                else 0
            ),
            "pending_reviews": pending_reviews,
            "state_compliance": state_compliance,
            "next_review": min(
                [c.next_review for c in self.sfg_compliance.values() if c.next_review],
                default=None,
            ),
        }

    def generate_compliance_report(
        self, framework: ComplianceFramework
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report for a framework"""
        if framework == ComplianceFramework.SOC2_TYPE2:
            return {
                "framework": "SOC 2 Type 2",
                "report_date": datetime.now(timezone.utc).isoformat(),
                "status": self.get_soc2_status(),
                "controls": [
                    {
                        "control_id": control.control_id,
                        "name": control.name,
                        "category": control.category.value,
                        "is_implemented": control.is_implemented,
                        "risk_level": control.risk_level,
                        "last_assessed": (
                            control.last_assessed.isoformat()
                            if control.last_assessed
                            else None
                        ),
                        "next_assessment": (
                            control.next_assessment.isoformat()
                            if control.next_assessment
                            else None
                        ),
                    }
                    for control in self.soc2_controls.values()
                ],
            }
        elif framework in [ComplianceFramework.GDPR, ComplianceFramework.CCPA]:
            return {
                "framework": framework.value.upper(),
                "report_date": datetime.now(timezone.utc).isoformat(),
                "status": self.get_gdpr_ccpa_status(),
                "data_flows": [
                    {
                        "flow_id": flow.flow_id,
                        "name": flow.name,
                        "data_categories": flow.data_categories,
                        "purposes": [p.value for p in flow.purposes],
                        "retention_period_days": flow.retention_period_days,
                        "legal_basis": flow.legal_basis,
                    }
                    for flow in self.data_flows.values()
                ],
            }
        elif framework == ComplianceFramework.SFG_INSURANCE:
            return {
                "framework": "SFG Insurance Compliance",
                "report_date": datetime.now(timezone.utc).isoformat(),
                "status": self.get_sfg_compliance_status(),
                "requirements": [
                    {
                        "compliance_id": compliance.compliance_id,
                        "requirement": compliance.requirement,
                        "compliance_status": compliance.compliance_status,
                        "risk_assessment": compliance.risk_assessment,
                        "last_reviewed": (
                            compliance.last_reviewed.isoformat()
                            if compliance.last_reviewed
                            else None
                        ),
                        "next_review": (
                            compliance.next_review.isoformat()
                            if compliance.next_review
                            else None
                        ),
                    }
                    for compliance in self.sfg_compliance.values()
                ],
            }

        return {}

    def _start_compliance_monitoring(self):
        """Start background task for compliance monitoring"""

        async def monitoring_task():
            while True:
                try:
                    # Check for overdue assessments
                    await self._check_overdue_assessments()

                    # Check for upcoming reviews
                    await self._check_upcoming_reviews()

                    # Run every 24 hours
                    await asyncio.sleep(86400)

                except Exception as e:
                    logger.error(f"Error in compliance monitoring: {e}")
                    await asyncio.sleep(3600)  # Wait 1 hour on error

        # Start the background task only if there's a running event loop
        try:
            loop = asyncio.get_running_loop()
            self._monitoring_task = loop.create_task(monitoring_task())
        except RuntimeError:
            # No running event loop, skip background task
            logger.debug("No running event loop, skipping compliance monitoring")
            self._monitoring_task = None

    async def _check_overdue_assessments(self):
        """Check for overdue SOC 2 assessments"""
        now = datetime.now(timezone.utc)
        overdue_controls = []

        for control in self.soc2_controls.values():
            if control.next_assessment and control.next_assessment < now:
                overdue_controls.append(control.control_id)

        if overdue_controls:
            logger.warning(
                f"Found {len(overdue_controls)} overdue SOC 2 assessments: {overdue_controls}"
            )

    async def _check_upcoming_reviews(self):
        """Check for upcoming compliance reviews"""
        now = datetime.now(timezone.utc)
        upcoming_reviews = []

        # Check SFG compliance reviews
        for compliance in self.sfg_compliance.values():
            if compliance.next_review and compliance.next_review < now + timedelta(
                days=7
            ):
                upcoming_reviews.append(f"SFG: {compliance.compliance_id}")

        if upcoming_reviews:
            logger.info(
                f"Found {len(upcoming_reviews)} upcoming compliance reviews: {upcoming_reviews}"
            )


# Global compliance manager instance
compliance_manager = ComplianceManager()
