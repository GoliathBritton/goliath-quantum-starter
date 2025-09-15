"""
FLYFOX AI Quantum Hub - Sigma Lead Mapper

Maps sales lead scoring problems to QUBO optimization format.
Used by Sigma Select for quantum-enhanced lead scoring.
"""

import numpy as np
from typing import Dict, Any, List, Optional
import logging

from .base_mapper import ProblemMapper

logger = logging.getLogger(__name__)


class SigmaLeadMapper(ProblemMapper):
    """
    Sigma Select Lead Scoring Mapper

    Converts sales lead scoring problems to QUBO format for quantum optimization.
    Optimizes lead prioritization, channel selection, and resource allocation.
    """

    def __init__(self):
        super().__init__(
            name="Sigma Lead Scoring Mapper",
            description="Maps sales lead scoring to QUBO for quantum optimization",
        )

        # Sigma Select specific parameters
        self.default_weights = {
            "engagement": 0.3,
            "budget": 0.25,
            "authority": 0.25,
            "timeline": 0.2,
        }

        self.channel_costs = {
            "email": 1.0,
            "phone": 5.0,
            "linkedin": 2.0,
            "meeting": 20.0,
            "demo": 50.0,
        }

    async def map_to_qubo(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map lead scoring problem to QUBO format."""
        try:
            # Validate input
            if not await self.validate_input(problem_data):
                raise ValueError("Invalid lead scoring problem data")

            leads = problem_data["leads"]
            channels = problem_data.get("channels", ["email", "phone", "linkedin"])
            budget = problem_data.get("budget", 1000)
            max_leads = problem_data.get("max_leads", len(leads))

            n_leads = len(leads)
            n_channels = len(channels)
            total_vars = n_leads + n_leads * n_channels  # x_i + y_ij variables

            # Initialize QUBO matrix
            qubo_matrix = np.zeros((total_vars, total_vars))
            linear_terms = np.zeros(total_vars)

            # Variable mapping:
            # x_i: Whether to contact lead i (0 to n_leads-1)
            # y_ij: Whether to use channel j for lead i (n_leads to total_vars-1)

            # Objective: Maximize expected revenue - contact costs
            for i, lead in enumerate(leads):
                # Lead selection variable x_i
                expected_revenue = self._calculate_expected_revenue(lead)
                linear_terms[i] = -expected_revenue  # Negative because we minimize

                # Channel selection variables y_ij
                for j, channel in enumerate(channels):
                    y_idx = n_leads + i * n_channels + j
                    channel_cost = self.channel_costs.get(channel, 1.0)
                    linear_terms[y_idx] = channel_cost

            # Constraints

            # 1. Budget constraint: sum of channel costs <= budget
            budget_penalty = 1000  # Large penalty for budget violation
            for i in range(n_leads):
                for j, channel in enumerate(channels):
                    y_idx = n_leads + i * n_channels + j
                    channel_cost = self.channel_costs.get(channel, 1.0)

                    # Add quadratic terms for budget constraint
                    for i2 in range(n_leads):
                        for j2, channel2 in enumerate(channels):
                            y2_idx = n_leads + i2 * n_channels + j2
                            channel_cost2 = self.channel_costs.get(channel2, 1.0)

                            if y_idx <= y2_idx:  # Avoid double counting
                                qubo_matrix[y_idx][y2_idx] += (
                                    budget_penalty * channel_cost * channel_cost2
                                )

            # 2. Lead-channel coupling: y_ij <= x_i
            coupling_penalty = 500
            for i in range(n_leads):
                for j in range(n_channels):
                    y_idx = n_leads + i * n_channels + j
                    # y_ij - x_i <= 0 becomes y_ij^2 - y_ij*x_i
                    qubo_matrix[y_idx][y_idx] += coupling_penalty  # y_ij^2 term
                    qubo_matrix[i][y_idx] -= coupling_penalty  # -y_ij*x_i term

            # 3. Maximum leads constraint
            if max_leads < n_leads:
                max_leads_penalty = 800
                for i in range(n_leads):
                    for j in range(n_leads):
                        if i <= j:
                            qubo_matrix[i][j] += max_leads_penalty

            # 4. Channel exclusivity: at most one channel per lead
            exclusivity_penalty = 300
            for i in range(n_leads):
                for j1 in range(n_channels):
                    for j2 in range(j1 + 1, n_channels):
                        y1_idx = n_leads + i * n_channels + j1
                        y2_idx = n_leads + i * n_channels + j2
                        qubo_matrix[y1_idx][y2_idx] += exclusivity_penalty

            # Add constant term for budget constraint
            constant_term = budget_penalty * budget * budget

            result = {
                "qubo_matrix": qubo_matrix.tolist(),
                "linear_terms": linear_terms.tolist(),
                "constant_term": constant_term,
                "metadata": {
                    "mapper": self.name,
                    "problem_type": "lead_scoring",
                    "n_leads": n_leads,
                    "n_channels": n_channels,
                    "total_variables": total_vars,
                    "budget": budget,
                    "max_leads": max_leads,
                    "branding": "Sigma Select - FLYFOX AI Quantum",
                },
            }

            logger.info(
                f"Sigma Lead Mapper: Mapped {n_leads} leads to {total_vars} QUBO variables"
            )
            return result

        except Exception as e:
            logger.error(f"Sigma Lead Mapper failed: {e}")
            raise

    async def validate_input(self, problem_data: Dict[str, Any]) -> bool:
        """Validate lead scoring problem data."""
        required_fields = ["leads"]
        if not all(field in problem_data for field in required_fields):
            return False

        leads = problem_data["leads"]
        if not isinstance(leads, list) or len(leads) == 0:
            return False

        # Validate each lead
        for lead in leads:
            if not isinstance(lead, dict):
                return False

            # Check for required lead fields
            required_lead_fields = [
                "id",
                "engagement_score",
                "budget_score",
                "authority_score",
            ]
            if not all(field in lead for field in required_lead_fields):
                return False

            # Validate scores are between 0 and 1
            for field in required_lead_fields[1:]:  # Skip 'id'
                score = lead[field]
                if not isinstance(score, (int, float)) or score < 0 or score > 1:
                    return False

        # Validate optional fields
        if "budget" in problem_data:
            budget = problem_data["budget"]
            if not isinstance(budget, (int, float)) or budget <= 0:
                return False

        if "max_leads" in problem_data:
            max_leads = problem_data["max_leads"]
            if not isinstance(max_leads, int) or max_leads <= 0:
                return False

        return True

    async def estimate_problem_size(self, problem_data: Dict[str, Any]) -> int:
        """Estimate the size of the resulting QUBO problem."""
        if not await self.validate_input(problem_data):
            return 0

        leads = problem_data["leads"]
        channels = problem_data.get("channels", ["email", "phone", "linkedin"])

        n_leads = len(leads)
        n_channels = len(channels)

        # Variables: x_i (leads) + y_ij (lead-channel combinations)
        total_vars = n_leads + n_leads * n_channels

        return total_vars

    def _calculate_expected_revenue(self, lead: Dict[str, Any]) -> float:
        """Calculate expected revenue for a lead."""
        engagement = lead.get("engagement_score", 0)
        budget = lead.get("budget_score", 0)
        authority = lead.get("authority_score", 0)
        timeline = lead.get("timeline_score", 0.5)

        # Weighted combination of scores
        weights = self.default_weights
        weighted_score = (
            engagement * weights["engagement"]
            + budget * weights["budget"]
            + authority * weights["authority"]
            + timeline * weights["timeline"]
        )

        # Convert to expected revenue (simplified model)
        base_revenue = lead.get("base_revenue", 10000)
        expected_revenue = weighted_score * base_revenue

        return expected_revenue

    async def interpret_solution(
        self, solution: Dict[str, Any], problem_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Interpret QUBO solution back to lead scoring results."""
        try:
            solution_vector = solution.get("solution_vector", [])
            leads = problem_data["leads"]
            channels = problem_data.get("channels", ["email", "phone", "linkedin"])

            n_leads = len(leads)
            n_channels = len(channels)

            # Extract lead selection variables
            selected_leads = []
            lead_channels = {}

            for i, lead in enumerate(leads):
                if i < len(solution_vector) and solution_vector[i] == 1:
                    selected_leads.append(lead)

                    # Find selected channel for this lead
                    for j, channel in enumerate(channels):
                        y_idx = n_leads + i * n_channels + j
                        if y_idx < len(solution_vector) and solution_vector[y_idx] == 1:
                            lead_channels[lead["id"]] = channel
                            break

            # Calculate metrics
            total_cost = sum(
                self.channel_costs.get(lead_channels.get(lead["id"], "email"), 1.0)
                for lead in selected_leads
            )

            total_expected_revenue = sum(
                self._calculate_expected_revenue(lead) for lead in selected_leads
            )

            roi = (
                (total_expected_revenue - total_cost) / total_cost
                if total_cost > 0
                else 0
            )

            return {
                "selected_leads": selected_leads,
                "lead_channels": lead_channels,
                "total_cost": total_cost,
                "total_expected_revenue": total_expected_revenue,
                "roi": roi,
                "num_leads_selected": len(selected_leads),
                "metadata": {
                    "mapper": self.name,
                    "branding": "Sigma Select - FLYFOX AI Quantum",
                },
            }

        except Exception as e:
            logger.error(f"Sigma Lead Mapper solution interpretation failed: {e}")
            raise
