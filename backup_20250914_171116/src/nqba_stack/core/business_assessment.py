"""
NQBA Business Assessment Engine
Comprehensive business evaluation integrating IBP, BEMs, and quantum optimization
Provides quantum-enhanced business intelligence and assessment capabilities
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

from .settings import get_settings
from .ltc_logger import get_ltc_logger

logger = logging.getLogger(__name__)

class AuditType(Enum):
    """Types of business audits supported by NQBA"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    IT_SECURITY = "it_security"
    SMETA = "smeta"
    STRATEGIC = "strategic"
    RISK = "risk"
    SUSTAINABILITY = "sustainability"

class BEMFramework(Enum):
    """Business Excellence Model frameworks"""
    BALDRIGE = "baldrige"
    EFQM = "efqm"
    ISO_9001 = "iso_9001"
    SIX_SIGMA = "six_sigma"
    LEAN = "lean"

@dataclass
class AssessmentCriteria:
    """Assessment criteria for business evaluation"""
    category: str
    subcategory: str
    criteria: str
    weight: float
    quantum_optimizable: bool
    target_score: float
    current_score: Optional[float] = None

@dataclass
class AssessmentResult:
    """Result of a business assessment"""
    assessment_id: str
    timestamp: datetime
    audit_type: AuditType
    framework: Optional[BEMFramework]
    overall_score: float
    category_scores: Dict[str, float]
    recommendations: List[str]
    quantum_enhanced: bool
    ltc_reference: str
    next_assessment_date: datetime

class NQBABusinessAssessment:
    """NQBA Business Assessment Engine"""
    
    def __init__(self):
        """Initialize the business assessment engine"""
        self.settings = get_settings()
        self.ltc_logger = get_ltc_logger()
        
        # Initialize assessment frameworks
        self.baldrige_criteria = self._initialize_baldrige_criteria()
        self.efqm_criteria = self._initialize_efqm_criteria()
        self.ibp_framework = self._initialize_ibp_framework()
        
    def _initialize_baldrige_criteria(self) -> List[AssessmentCriteria]:
        """Initialize Baldrige Excellence Framework criteria"""
        return [
            # Leadership (150 points)
            AssessmentCriteria("Leadership", "Senior Leadership", "Vision and Values", 0.15, True, 85.0),
            AssessmentCriteria("Leadership", "Governance", "Legal and Ethical Behavior", 0.10, True, 90.0),
            AssessmentCriteria("Leadership", "Social Responsibility", "Community Support", 0.05, False, 80.0),
            
            # Strategy (85 points)
            AssessmentCriteria("Strategy", "Strategy Development", "Strategic Planning Process", 0.12, True, 85.0),
            AssessmentCriteria("Strategy", "Strategy Implementation", "Action Plan Development", 0.08, True, 80.0),
            
            # Customers (85 points)
            AssessmentCriteria("Customers", "Customer Engagement", "Customer Listening", 0.10, True, 85.0),
            AssessmentCriteria("Customers", "Voice of the Customer", "Customer Satisfaction", 0.10, True, 85.0),
            
            # Measurement, Analysis, and Knowledge Management (90 points)
            AssessmentCriteria("Measurement", "Performance Measurement", "Data Collection", 0.08, True, 85.0),
            AssessmentCriteria("Measurement", "Performance Analysis", "Comparative Analysis", 0.08, True, 85.0),
            AssessmentCriteria("Measurement", "Knowledge Management", "Organizational Learning", 0.04, False, 80.0),
            
            # Workforce (85 points)
            AssessmentCriteria("Workforce", "Workforce Environment", "Workplace Climate", 0.08, True, 85.0),
            AssessmentCriteria("Workforce", "Workforce Engagement", "Employee Development", 0.08, True, 85.0),
            
            # Operations (85 points)
            AssessmentCriteria("Operations", "Work Systems", "Core Competencies", 0.08, True, 85.0),
            AssessmentCriteria("Operations", "Work Processes", "Process Management", 0.08, True, 85.0),
            
            # Results (450 points)
            AssessmentCriteria("Results", "Product and Process Results", "Product Performance", 0.15, True, 85.0),
            AssessmentCriteria("Results", "Customer-Focused Results", "Customer Satisfaction", 0.10, True, 85.0),
            AssessmentCriteria("Results", "Workforce-Focused Results", "Employee Engagement", 0.08, True, 85.0),
            AssessmentCriteria("Results", "Leadership and Governance Results", "Financial Performance", 0.12, True, 85.0),
        ]
    
    def _initialize_efqm_criteria(self) -> List[AssessmentCriteria]:
        """Initialize EFQM Excellence Model criteria"""
        return [
            # Enablers (50%)
            AssessmentCriteria("Leadership", "Strategic Direction", "Vision and Mission", 0.10, True, 85.0),
            AssessmentCriteria("People", "People Strategy", "Employee Development", 0.08, True, 85.0),
            AssessmentCriteria("Partnerships", "Stakeholder Management", "Supplier Relationships", 0.08, True, 85.0),
            AssessmentCriteria("Processes", "Process Management", "Operational Excellence", 0.12, True, 85.0),
            AssessmentCriteria("Resources", "Financial Management", "Asset Optimization", 0.12, True, 85.0),
            
            # Results (50%)
            AssessmentCriteria("Results", "Customer Results", "Customer Satisfaction", 0.15, True, 85.0),
            AssessmentCriteria("Results", "People Results", "Employee Satisfaction", 0.10, True, 85.0),
            AssessmentCriteria("Results", "Society Results", "Social Impact", 0.05, False, 80.0),
            AssessmentCriteria("Results", "Business Results", "Financial Performance", 0.20, True, 85.0),
        ]
    
    def _initialize_ibp_framework(self) -> Dict[str, Any]:
        """Initialize Integrated Business Planning framework"""
        return {
            "strategic_alignment": {
                "description": "Unifies business strategy with planning, budgeting, and forecasting",
                "components": ["vision_alignment", "goal_cascading", "resource_allocation"],
                "quantum_optimizable": True,
                "weight": 0.25
            },
            "cross_functional_collaboration": {
                "description": "Breaks down departmental silos through integrated data and analysis",
                "components": ["data_integration", "collaborative_planning", "shared_objectives"],
                "quantum_optimizable": True,
                "weight": 0.20
            },
            "long_term_focus": {
                "description": "24-60 month rolling horizon for proactive decision-making",
                "components": ["scenario_planning", "forecasting", "trend_analysis"],
                "quantum_optimizable": True,
                "weight": 0.25
            },
            "risk_resilience": {
                "description": "Integrated risk assessments for disruption resilience",
                "components": ["risk_identification", "mitigation_strategies", "stress_testing"],
                "quantum_optimizable": True,
                "weight": 0.30
            }
        }
    
    async def assess_business_comprehensive(
        self,
        company_data: Dict[str, Any],
        audit_types: List[AuditType] = None,
        framework: BEMFramework = BEMFramework.BALDRIGE,
        use_quantum: bool = True
    ) -> AssessmentResult:
        """Perform comprehensive business assessment using quantum optimization"""
        
        if audit_types is None:
            audit_types = [AuditType.FINANCIAL, AuditType.OPERATIONAL, AuditType.COMPLIANCE]
        
        try:
            # Log assessment start
            ltc_ref = self.ltc_logger.log_operation(
                operation_type="business_assessment_started",
                operation_data={
                    "company_data": company_data,
                    "audit_types": [at.value for at in audit_types],
                    "framework": framework.value,
                    "use_quantum": use_quantum
                },
                thread_ref="BUSINESS_ASSESSMENT"
            )
            
            # Perform individual audits
            audit_results = {}
            for audit_type in audit_types:
                audit_results[audit_type.value] = await self._perform_audit(
                    audit_type, company_data, use_quantum
                )
            
            # Apply BEM framework
            bem_results = await self._apply_bem_framework(
                framework, company_data, audit_results, use_quantum
            )
            
            # Apply IBP framework
            ibp_results = await self._apply_ibp_framework(
                company_data, audit_results, bem_results, use_quantum
            )
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(audit_results, bem_results, ibp_results)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                audit_results, bem_results, ibp_results, overall_score
            )
            
            # Create assessment result
            assessment_result = AssessmentResult(
                assessment_id=f"ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                audit_type=audit_types[0] if len(audit_types) == 1 else None,
                framework=framework,
                overall_score=overall_score,
                category_scores={
                    **{f"audit_{k}": v["score"] for k, v in audit_results.items()},
                    **{f"bem_{k}": v for k, v in bem_results.items()},
                    **{f"ibp_{k}": v for k, v in ibp_results.items()}
                },
                recommendations=recommendations,
                quantum_enhanced=use_quantum,
                ltc_reference=ltc_ref,
                next_assessment_date=datetime.now() + timedelta(days=90)
            )
            
            # Log assessment completion
            self.ltc_logger.log_operation(
                operation_type="business_assessment_completed",
                operation_data={
                    "assessment_id": assessment_result.assessment_id,
                    "overall_score": overall_score,
                    "recommendations_count": len(recommendations),
                    "quantum_enhanced": use_quantum
                },
                thread_ref="BUSINESS_ASSESSMENT"
            )
            
            return assessment_result
            
        except Exception as e:
            logger.error(f"Business assessment failed: {e}")
            raise
    
    async def _perform_audit(
        self, 
        audit_type: AuditType, 
        company_data: Dict[str, Any], 
        use_quantum: bool
    ) -> Dict[str, Any]:
        """Perform specific audit type"""
        
        if audit_type == AuditType.FINANCIAL:
            return await self._financial_audit(company_data, use_quantum)
        elif audit_type == AuditType.OPERATIONAL:
            return await self._operational_audit(company_data, use_quantum)
        elif audit_type == AuditType.COMPLIANCE:
            return await self._compliance_audit(company_data, use_quantum)
        elif audit_type == AuditType.IT_SECURITY:
            return await self._it_security_audit(company_data, use_quantum)
        elif audit_type == AuditType.SMETA:
            return await self._smeta_audit(company_data, use_quantum)
        else:
            return {"score": 75.0, "findings": [], "risk_level": "medium"}
    
    async def _financial_audit(self, company_data: Dict[str, Any], use_quantum: bool) -> Dict[str, Any]:
        """Perform financial audit with quantum optimization"""
        
        # Extract financial metrics
        revenue = company_data.get("revenue", 0)
        expenses = company_data.get("expenses", 0)
        assets = company_data.get("assets", 0)
        liabilities = company_data.get("liabilities", 0)
        
        # Calculate financial ratios
        profit_margin = (revenue - expenses) / revenue if revenue > 0 else 0
        debt_ratio = liabilities / assets if assets > 0 else 0
        current_ratio = company_data.get("current_assets", 0) / company_data.get("current_liabilities", 1)
        
        # Quantum optimization for financial scoring
        if use_quantum and self.settings.dynex_configured:
            # Use quantum optimization to weight financial factors
            financial_factors = [profit_margin, 1 - debt_ratio, min(current_ratio / 2, 1)]
            score = await self._quantum_optimize_financial_score(financial_factors)
        else:
            # Classical scoring
            score = (profit_margin * 0.4 + (1 - debt_ratio) * 0.3 + min(current_ratio / 2, 1) * 0.3) * 100
        
        return {
            "score": min(max(score, 0), 100),
            "findings": [
                f"Profit margin: {profit_margin:.2%}",
                f"Debt ratio: {debt_ratio:.2%}",
                f"Current ratio: {current_ratio:.2f}"
            ],
            "risk_level": "low" if score > 80 else "medium" if score > 60 else "high"
        }
    
    async def _operational_audit(self, company_data: Dict[str, Any], use_quantum: bool) -> Dict[str, Any]:
        """Perform operational audit with quantum optimization"""
        
        # Extract operational metrics
        efficiency = company_data.get("operational_efficiency", 0.75)
        productivity = company_data.get("productivity_score", 0.80)
        quality_score = company_data.get("quality_score", 0.85)
        
        # Quantum optimization for operational scoring
        if use_quantum and self.settings.dynex_configured:
            operational_factors = [efficiency, productivity, quality_score]
            score = await self._quantum_optimize_operational_score(operational_factors)
        else:
            # Classical scoring
            score = (efficiency * 0.4 + productivity * 0.3 + quality_score * 0.3) * 100
        
        return {
            "score": min(max(score, 0), 100),
            "findings": [
                f"Operational efficiency: {efficiency:.2%}",
                f"Productivity score: {productivity:.2%}",
                f"Quality score: {quality_score:.2%}"
            ],
            "risk_level": "low" if score > 80 else "medium" if score > 60 else "high"
        }
    
    async def _compliance_audit(self, company_data: Dict[str, Any], use_quantum: bool) -> Dict[str, Any]:
        """Perform compliance audit"""
        
        # Extract compliance metrics
        regulatory_compliance = company_data.get("regulatory_compliance", 0.90)
        internal_policies = company_data.get("internal_policies", 0.85)
        ethical_standards = company_data.get("ethical_standards", 0.95)
        
        score = (regulatory_compliance * 0.4 + internal_policies * 0.3 + ethical_standards * 0.3) * 100
        
        return {
            "score": min(max(score, 0), 100),
            "findings": [
                f"Regulatory compliance: {regulatory_compliance:.2%}",
                f"Internal policies: {internal_policies:.2%}",
                f"Ethical standards: {ethical_standards:.2%}"
            ],
            "risk_level": "low" if score > 90 else "medium" if score > 70 else "high"
        }
    
    async def _apply_bem_framework(
        self, 
        framework: BEMFramework, 
        company_data: Dict[str, Any], 
        audit_results: Dict[str, Any],
        use_quantum: bool
    ) -> Dict[str, float]:
        """Apply Business Excellence Model framework"""
        
        if framework == BEMFramework.BALDRIGE:
            criteria = self.baldrige_criteria
        elif framework == BEMFramework.EFQM:
            criteria = self.efqm_criteria
        else:
            criteria = self.baldrige_criteria  # Default to Baldrige
        
        category_scores = {}
        
        for criterion in criteria:
            # Calculate score for each criterion
            if use_quantum and criterion.quantum_optimizable and self.settings.dynex_configured:
                score = await self._quantum_optimize_criterion(criterion, company_data)
            else:
                score = self._classical_criterion_score(criterion, company_data)
            
            # Aggregate by category
            if criterion.category not in category_scores:
                category_scores[criterion.category] = []
            category_scores[criterion.category].append(score * criterion.weight)
        
        # Calculate weighted category scores
        return {category: sum(scores) for category, scores in category_scores.items()}
    
    async def _apply_ibp_framework(
        self, 
        company_data: Dict[str, Any], 
        audit_results: Dict[str, Any],
        bem_results: Dict[str, float],
        use_quantum: bool
    ) -> Dict[str, float]:
        """Apply Integrated Business Planning framework"""
        
        ibp_scores = {}
        
        for component, config in self.ibp_framework.items():
            if use_quantum and config["quantum_optimizable"] and self.settings.dynex_configured:
                score = await self._quantum_optimize_ibp_component(component, company_data, audit_results, bem_results)
            else:
                score = self._classical_ibp_component_score(component, company_data, audit_results, bem_results)
            
            ibp_scores[component] = score * config["weight"]
        
        return ibp_scores
    
    def _calculate_overall_score(
        self, 
        audit_results: Dict[str, Any], 
        bem_results: Dict[str, float],
        ibp_results: Dict[str, float]
    ) -> float:
        """Calculate overall assessment score"""
        
        # Weight the different components
        audit_weight = 0.4
        bem_weight = 0.35
        ibp_weight = 0.25
        
        # Calculate weighted scores
        audit_score = sum(result["score"] for result in audit_results.values()) / len(audit_results)
        bem_score = sum(bem_results.values()) * 100  # Convert to percentage
        ibp_score = sum(ibp_results.values()) * 100  # Convert to percentage
        
        overall_score = (
            audit_score * audit_weight +
            bem_score * bem_weight +
            ibp_score * ibp_weight
        )
        
        return min(max(overall_score, 0), 100)
    
    def _generate_recommendations(
        self, 
        audit_results: Dict[str, Any], 
        bem_results: Dict[str, float],
        ibp_results: Dict[str, float],
        overall_score: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Overall performance recommendations
        if overall_score < 60:
            recommendations.append("🚨 CRITICAL: Implement immediate improvement plan across all business areas")
        elif overall_score < 80:
            recommendations.append("⚠️ PRIORITY: Focus on high-impact areas for improvement")
        else:
            recommendations.append("✅ EXCELLENT: Maintain current performance and focus on continuous improvement")
        
        # Audit-specific recommendations
        for audit_type, result in audit_results.items():
            if result["score"] < 70:
                recommendations.append(f"🔧 {audit_type.title()}: Address identified risks and implement controls")
        
        # BEM-specific recommendations
        for category, score in bem_results.items():
            if score < 0.7:  # 70% threshold
                recommendations.append(f"📊 {category.title()}: Develop excellence improvement plan")
        
        # IBP-specific recommendations
        for component, score in ibp_results.items():
            if score < 0.7:  # 70% threshold
                recommendations.append(f"🎯 {component.replace('_', ' ').title()}: Enhance integrated planning capabilities")
        
        return recommendations
    
    # Quantum optimization methods (placeholder implementations)
    async def _quantum_optimize_financial_score(self, factors: List[float]) -> float:
        """Quantum optimization for financial scoring"""
        # Placeholder - would integrate with Dynex quantum computing
        return sum(factors) / len(factors) * 100
    
    async def _quantum_optimize_operational_score(self, factors: List[float]) -> float:
        """Quantum optimization for operational scoring"""
        # Placeholder - would integrate with Dynex quantum computing
        return sum(factors) / len(factors) * 100
    
    async def _quantum_optimize_criterion(self, criterion: AssessmentCriteria, company_data: Dict[str, Any]) -> float:
        """Quantum optimization for BEM criterion"""
        # Placeholder - would integrate with Dynex quantum computing
        return criterion.target_score / 100
    
    async def _quantum_optimize_ibp_component(self, component: str, company_data: Dict[str, Any], audit_results: Dict[str, Any], bem_results: Dict[str, float]) -> float:
        """Quantum optimization for IBP component"""
        # Placeholder - would integrate with Dynex quantum computing
        return 0.8  # 80% default score
    
    # Classical scoring methods
    def _classical_criterion_score(self, criterion: AssessmentCriteria, company_data: Dict[str, Any]) -> float:
        """Classical scoring for BEM criterion"""
        return criterion.target_score / 100
    
    def _classical_ibp_component_score(self, component: str, company_data: Dict[str, Any], audit_results: Dict[str, Any], bem_results: Dict[str, float]) -> float:
        """Classical scoring for IBP component"""
        return 0.8  # 80% default score

# Global instance
business_assessment = NQBABusinessAssessment()

# Convenience functions
async def assess_business_comprehensive(
    company_data: Dict[str, Any],
    audit_types: List[AuditType] = None,
    framework: BEMFramework = BEMFramework.BALDRIGE,
    use_quantum: bool = True
) -> AssessmentResult:
    """Perform comprehensive business assessment"""
    return await business_assessment.assess_business_comprehensive(
        company_data, audit_types, framework, use_quantum
    )
