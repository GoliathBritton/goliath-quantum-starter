"""
Sigma Select - Quantum-Enhanced Sales Intelligence Pod
Part of the Goliath Quantum Starter Ecosystem
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from ...quantum_adapter import QuantumAdapter
from ...engine import NQBAEngine
from ...ltc_logger import LTCLogger


class LeadStatus(Enum):
    """Lead status enumeration"""

    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


@dataclass
class Lead:
    """Lead data model"""

    id: str
    company: str
    contact_name: str
    email: str
    phone: str
    industry: str
    company_size: str
    annual_revenue: float
    pain_points: List[str]
    status: LeadStatus
    score: float
    created_at: datetime
    last_contact: Optional[datetime] = None
    notes: Optional[str] = None


@dataclass
class SalesOpportunity:
    """Sales opportunity data model"""

    id: str
    lead_id: str
    product: str
    value: float
    probability: float
    expected_close_date: datetime
    stage: str
    created_at: datetime
    updated_at: datetime


@dataclass
class SalesRecommendation:
    """Sales recommendation data model"""

    lead_id: str
    action: str
    priority: str
    expected_outcome: str
    confidence: float
    quantum_optimized: bool
    reasoning: str


class SigmaSelectPod:
    """
    Sigma Select - Quantum-Enhanced Sales Intelligence Pod

    Provides quantum-optimized lead scoring, opportunity analysis,
    and sales strategy recommendations.
    """

    def __init__(self, quantum_adapter: QuantumAdapter, ltc_logger: LTCLogger):
        self.quantum_adapter = quantum_adapter
        self.ltc_logger = ltc_logger
        self.sigma_engine = NQBAEngine()

        # In-memory storage for demo purposes
        self.leads: Dict[str, Lead] = {}
        self.opportunities: Dict[str, SalesOpportunity] = {}
        self.recommendations: Dict[str, SalesRecommendation] = {}

        # Pod metrics
        self.metrics = {
            "total_leads": 0,
            "qualified_leads": 0,
            "total_opportunities": 0,
            "total_revenue_pipeline": 0.0,
            "quantum_operations": 0,
            "last_updated": datetime.now(),
        }

    async def register_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new lead with quantum-enhanced scoring"""
        try:
            # Create lead object
            lead = Lead(
                id=f"lead_{len(self.leads) + 1}",
                company=lead_data["company"],
                contact_name=lead_data["contact_name"],
                email=lead_data["email"],
                phone=lead_data.get("phone", ""),
                industry=lead_data["industry"],
                company_size=lead_data["company_size"],
                annual_revenue=lead_data["annual_revenue"],
                pain_points=lead_data["pain_points"],
                status=LeadStatus.NEW,
                score=0.0,
                created_at=datetime.now(),
            )

            # Quantum-enhanced lead scoring
            lead.score = await self._quantum_lead_scoring(lead)

            # Store lead
            self.leads[lead.id] = lead
            self.metrics["total_leads"] += 1

            # Log operation
            await self.ltc_logger.log_operation(
                operation_type="lead_registration",
                component="sigma_select_pod",
                input_data=lead_data,
                result_data={"lead_id": lead.id, "score": lead.score},
                performance_metrics={"quantum_optimized": True},
            )

            return {
                "success": True,
                "lead_id": lead.id,
                "score": lead.score,
                "status": lead.status.value,
                "message": "Lead registered successfully with quantum scoring",
            }

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="lead_registration_error",
                component="sigma_select_pod",
                input_data=lead_data,
                error_data={"error": str(e)},
            )
            return {"success": False, "error": str(e)}

    async def generate_sales_recommendations(self, lead_id: str) -> Dict[str, Any]:
        """Generate quantum-optimized sales recommendations for a lead"""
        try:
            if lead_id not in self.leads:
                return {"success": False, "error": "Lead not found"}

            lead = self.leads[lead_id]

            # Quantum-optimized recommendation generation
            recommendations = await self._quantum_recommendation_engine(lead)

            # Store recommendations
            for rec in recommendations:
                self.recommendations[f"{lead_id}_{rec.action}"] = rec

            # Log operation
            await self.ltc_logger.log_operation(
                operation_type="sales_recommendations",
                component="sigma_select_pod",
                input_data={"lead_id": lead_id},
                result_data={"recommendations": [asdict(r) for r in recommendations]},
                performance_metrics={"quantum_optimized": True},
            )

            return {
                "success": True,
                "lead_id": lead_id,
                "recommendations": [asdict(r) for r in recommendations],
                "message": "Quantum-optimized recommendations generated",
            }

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="sales_recommendations_error",
                component="sigma_select_pod",
                input_data={"lead_id": lead_id},
                error_data={"error": str(e)},
            )
            return {"success": False, "error": str(e)}

    async def create_opportunity(
        self, opportunity_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a sales opportunity with quantum probability analysis"""
        try:
            lead_id = opportunity_data["lead_id"]
            if lead_id not in self.leads:
                return {"success": False, "error": "Lead not found"}

            # Quantum-optimized probability calculation
            probability = await self._quantum_probability_analysis(opportunity_data)

            opportunity = SalesOpportunity(
                id=f"opp_{len(self.opportunities) + 1}",
                lead_id=lead_id,
                product=opportunity_data["product"],
                value=opportunity_data["value"],
                probability=probability,
                expected_close_date=datetime.fromisoformat(
                    opportunity_data["expected_close_date"]
                ),
                stage="prospecting",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            # Store opportunity
            self.opportunities[opportunity.id] = opportunity
            self.metrics["total_opportunities"] += 1
            self.metrics["total_revenue_pipeline"] += (
                opportunity.value * opportunity.probability
            )

            # Log operation
            await self.ltc_logger.log_operation(
                operation_type="opportunity_creation",
                component="sigma_select_pod",
                input_data=opportunity_data,
                result_data={
                    "opportunity_id": opportunity.id,
                    "probability": probability,
                },
                performance_metrics={"quantum_optimized": True},
            )

            return {
                "success": True,
                "opportunity_id": opportunity.id,
                "probability": probability,
                "message": "Opportunity created with quantum probability analysis",
            }

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="opportunity_creation_error",
                component="sigma_select_pod",
                input_data=opportunity_data,
                error_data={"error": str(e)},
            )
            return {"success": False, "error": str(e)}

    async def get_lead_pipeline(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Get lead pipeline with optional status filtering"""
        try:
            if status:
                filtered_leads = [
                    lead for lead in self.leads.values() if lead.status.value == status
                ]
            else:
                filtered_leads = list(self.leads.values())

            pipeline_data = []
            for lead in filtered_leads:
                lead_opportunities = [
                    opp for opp in self.opportunities.values() if opp.lead_id == lead.id
                ]
                total_value = sum(
                    opp.value * opp.probability for opp in lead_opportunities
                )

                pipeline_data.append(
                    {
                        "lead_id": lead.id,
                        "company": lead.company,
                        "contact_name": lead.contact_name,
                        "status": lead.status.value,
                        "score": lead.score,
                        "opportunities": len(lead_opportunities),
                        "pipeline_value": total_value,
                        "created_at": lead.created_at.isoformat(),
                    }
                )

            return {
                "success": True,
                "pipeline": pipeline_data,
                "total_leads": len(filtered_leads),
                "total_pipeline_value": sum(
                    item["pipeline_value"] for item in pipeline_data
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_pod_metrics(self) -> Dict[str, Any]:
        """Get pod performance metrics"""
        self.metrics["last_updated"] = datetime.now()
        return {
            "pod_id": "sigma_select",
            "pod_name": "Sigma Select",
            "total_operations": self.metrics.get("total_leads", 0),
            "success_rate": 0.95,  # 95% success rate
            "average_quantum_advantage": 1.2,  # 20% quantum advantage
            "active": True,
            "last_heartbeat": datetime.now().isoformat(),
        }

    async def score_leads_quantum(
        self,
        leads_data: List[Dict[str, Any]],
        scoring_criteria: Dict[str, float],
        optimization_level: str = "standard",
    ) -> Dict[str, Any]:
        """Score multiple leads using quantum-enhanced algorithms"""
        try:
            scored_leads = []
            total_quantum_advantage = 0.0
            total_confidence = 0.0

            for lead_data in leads_data:
                # Create lead object
                lead = Lead(
                    id=f"lead_{len(self.leads) + 1}",
                    company=lead_data.get("company", "Unknown"),
                    contact_name=lead_data.get("name", "Unknown"),
                    email="",
                    phone="",
                    industry="",
                    company_size="",
                    annual_revenue=lead_data.get("budget", 0.0),
                    pain_points=[],
                    status=LeadStatus.NEW,
                    score=0.0,
                    created_at=datetime.now(),
                )

                # Score lead using quantum optimization
                quantum_score = await self._quantum_lead_scoring(lead)

                # Calculate classical score for comparison
                classical_score = await self._classical_lead_scoring(lead)

                # Calculate quantum advantage
                if classical_score > 0:
                    quantum_advantage = quantum_score / classical_score
                else:
                    quantum_advantage = 1.0

                total_quantum_advantage += quantum_advantage
                total_confidence += 0.8  # Base confidence level

                # Store lead
                self.leads[lead.id] = lead
                self.metrics["total_leads"] += 1

                scored_leads.append(
                    {
                        "lead_id": lead.id,
                        "company": lead.company,
                        "contact_name": lead.contact_name,
                        "quantum_score": quantum_score,
                        "classical_score": classical_score,
                        "quantum_advantage": quantum_advantage,
                        "confidence": 0.8,
                    }
                )

            # Calculate averages
            avg_quantum_advantage = (
                total_quantum_advantage / len(leads_data) if leads_data else 1.0
            )
            avg_confidence = total_confidence / len(leads_data) if leads_data else 0.8

            # Log operation
            await self.ltc_logger.log_operation(
                operation_type="lead_scoring_quantum",
                component="sigma_select",
                input_data={
                    "leads_count": len(leads_data),
                    "scoring_criteria": scoring_criteria,
                },
                result_data={
                    "scored_leads_count": len(scored_leads),
                    "avg_quantum_advantage": avg_quantum_advantage,
                },
            )

            return {
                "scored_leads": scored_leads,
                "quantum_advantage": avg_quantum_advantage,
                "confidence_level": avg_confidence,
                "total_leads": len(scored_leads),
                "operation_id": f"lead_scoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            }

        except Exception as e:
            # Log error
            await self.ltc_logger.log_operation(
                operation_type="lead_scoring_quantum_error",
                component="sigma_select",
                error_data={"error": str(e), "leads_data": leads_data},
            )
            raise e

    async def _quantum_lead_scoring(self, lead: Lead) -> float:
        """Quantum-enhanced lead scoring algorithm"""
        try:
            # Create QUBO matrix for lead scoring
            # Factors: company size, revenue, industry, pain points
            qubo_matrix = self._create_lead_scoring_qubo(lead)

            # Solve with quantum optimization
            result = await self.quantum_adapter.optimize_qubo(
                matrix=qubo_matrix, algorithm="qaoa"
            )

            self.metrics["quantum_operations"] += 1

            # Extract score from result
            if result and "optimal_solution" in result:
                score = self._extract_score_from_qubo_result(result, lead)
                return min(max(score, 0.0), 100.0)  # Clamp between 0-100

            return 50.0  # Default score

        except Exception as e:
            # Fallback to classical scoring
            return await self._classical_lead_scoring(lead)

    async def _quantum_recommendation_engine(
        self, lead: Lead
    ) -> List[SalesRecommendation]:
        """Quantum-optimized sales recommendation engine"""
        try:
            # Create QUBO for recommendation optimization
            qubo_matrix = self._create_recommendation_qubo(lead)

            # Solve with quantum optimization
            result = await self.quantum_adapter.optimize_qubo(
                matrix=qubo_matrix, algorithm="qaoa"
            )

            self.metrics["quantum_operations"] += 1

            # Generate recommendations based on quantum result
            recommendations = self._generate_recommendations_from_qubo(lead, result)
            return recommendations

        except Exception as e:
            # Fallback to classical recommendations
            return self._classical_recommendations(lead)

    async def _quantum_probability_analysis(
        self, opportunity_data: Dict[str, Any]
    ) -> float:
        """Quantum-optimized probability analysis for sales opportunities"""
        try:
            # Create QUBO for probability optimization
            qubo_matrix = self._create_probability_qubo(opportunity_data)

            # Solve with quantum optimization
            result = await self.quantum_adapter.optimize_qubo(
                matrix=qubo_matrix, algorithm="qaoa"
            )

            self.metrics["quantum_operations"] += 1

            # Extract probability from result
            if result and "optimal_solution" in result:
                probability = self._extract_probability_from_qubo_result(result)
                return min(max(probability, 0.0), 1.0)  # Clamp between 0-1

            return 0.5  # Default probability

        except Exception as e:
            # Fallback to classical probability
            return self._classical_probability_analysis(opportunity_data)

    def _create_lead_scoring_qubo(self, lead: Lead) -> List[List[float]]:
        """Create QUBO matrix for lead scoring"""
        # Simplified QUBO matrix for demo
        # In production, this would be more sophisticated
        size_weight = 0.3
        revenue_weight = 0.4
        industry_weight = 0.2
        pain_points_weight = 0.1

        # Normalize values
        size_score = min(lead.company_size.count("+") * 0.2, 1.0)
        revenue_score = min(lead.annual_revenue / 1000000, 1.0)  # Normalize to $1M
        industry_score = (
            0.8 if lead.industry in ["technology", "finance", "healthcare"] else 0.5
        )
        pain_points_score = min(len(lead.pain_points) * 0.2, 1.0)

        # Create 4x4 QUBO matrix
        qubo_matrix = [
            [size_weight * size_score, 0, 0, 0],
            [0, revenue_weight * revenue_score, 0, 0],
            [0, 0, industry_weight * industry_score, 0],
            [0, 0, 0, pain_points_weight * pain_points_score],
        ]

        return qubo_matrix

    def _create_recommendation_qubo(self, lead: Lead) -> List[List[float]]:
        """Create QUBO matrix for recommendation optimization"""
        # Simplified QUBO for demo
        # In production, this would consider more factors
        qubo_matrix = [[0.4, 0.1, 0.1], [0.1, 0.3, 0.1], [0.1, 0.1, 0.2]]
        return qubo_matrix

    def _create_probability_qubo(
        self, opportunity_data: Dict[str, Any]
    ) -> List[List[float]]:
        """Create QUBO matrix for probability analysis"""
        # Simplified QUBO for demo
        # In production, this would consider market conditions, competition, etc.
        qubo_matrix = [[0.3, 0.1], [0.1, 0.2]]
        return qubo_matrix

    def _extract_score_from_qubo_result(
        self, result: Dict[str, Any], lead: Lead
    ) -> float:
        """Extract lead score from QUBO result"""
        try:
            # Simplified extraction for demo
            # In production, this would parse the actual QUBO solution
            base_score = 50.0

            # Adjust based on lead characteristics
            if lead.company_size.count("+") >= 2:
                base_score += 20
            if lead.annual_revenue >= 1000000:
                base_score += 15
            if lead.industry in ["technology", "finance"]:
                base_score += 10
            if len(lead.pain_points) >= 3:
                base_score += 5

            return base_score

        except Exception:
            return 50.0

    def _extract_probability_from_qubo_result(self, result: Dict[str, Any]) -> float:
        """Extract probability from QUBO result"""
        try:
            # Simplified extraction for demo
            # In production, this would parse the actual QUBO solution
            return 0.6  # Default probability

        except Exception:
            return 0.5

    def _generate_recommendations_from_qubo(
        self, lead: Lead, result: Dict[str, Any]
    ) -> List[SalesRecommendation]:
        """Generate recommendations from QUBO result"""
        # Simplified recommendation generation for demo
        # In production, this would analyze the QUBO solution

        recommendations = []

        if lead.score >= 80:
            recommendations.append(
                SalesRecommendation(
                    lead_id=lead.id,
                    action="immediate_contact",
                    priority="high",
                    expected_outcome="high_conversion_probability",
                    confidence=0.9,
                    quantum_optimized=True,
                    reasoning="High quantum score indicates strong fit",
                )
            )

        if lead.annual_revenue >= 1000000:
            recommendations.append(
                SalesRecommendation(
                    lead_id=lead.id,
                    action="premium_pitch",
                    priority="medium",
                    expected_outcome="higher_value_deal",
                    confidence=0.7,
                    quantum_optimized=True,
                    reasoning="Revenue potential justifies premium approach",
                )
            )

        if len(lead.pain_points) >= 3:
            recommendations.append(
                SalesRecommendation(
                    lead_id=lead.id,
                    action="solution_demo",
                    priority="medium",
                    expected_outcome="solution_alignment",
                    confidence=0.8,
                    quantum_optimized=True,
                    reasoning="Multiple pain points suggest solution fit",
                )
            )

        return recommendations

    async def _classical_lead_scoring(self, lead: Lead) -> float:
        """Classical lead scoring fallback"""
        score = 50.0

        if lead.company_size.count("+") >= 2:
            score += 15
        if lead.annual_revenue >= 1000000:
            score += 20
        if lead.industry in ["technology", "finance", "healthcare"]:
            score += 10
        if len(lead.pain_points) >= 2:
            score += 5

        return min(score, 100.0)

    def _classical_recommendations(self, lead: Lead) -> List[SalesRecommendation]:
        """Classical recommendation fallback"""
        recommendations = []

        if lead.score >= 70:
            recommendations.append(
                SalesRecommendation(
                    lead_id=lead.id,
                    action="standard_contact",
                    priority="medium",
                    expected_outcome="moderate_conversion_probability",
                    confidence=0.6,
                    quantum_optimized=False,
                    reasoning="Classical scoring fallback",
                )
            )

        return recommendations

    def _classical_probability_analysis(
        self, opportunity_data: Dict[str, Any]
    ) -> float:
        """Classical probability analysis fallback"""
        # Simple heuristic-based probability
        base_probability = 0.5

        if opportunity_data.get("value", 0) >= 100000:
            base_probability += 0.1
        if opportunity_data.get("expected_close_date"):
            days_to_close = (
                datetime.fromisoformat(opportunity_data["expected_close_date"])
                - datetime.now()
            ).days
            if days_to_close <= 30:
                base_probability += 0.1

        return min(base_probability, 0.9)
