"""
Quantum Sales Navigator - Predictive deal pathfinding with REVERSAL REASONINGâ„¢
"""

from typing import Dict, Any, List, Optional
from app.nqba.qdllm import QDLLM
from app.nqba.dynex_adapter import DynexAdapter
from app.core.logging import get_logger

logger = get_logger(__name__)

class QuantumSalesNavigator:
    """
    Guides complex deal cycles with predictive navigation
    REVERSAL REASONINGâ„¢ enforces backward/forward coherence across steps
    """
    
    def __init__(self):
        self.qdllm = QDLLM()
        self.dynex = DynexAdapter()
        self.agent_id = "quantum_sales_navigator"
        self.tier_required = "ScaleUp"  # Minimum tier for this agent
    
    def recommend_path(self, opportunity_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend optimal sales path for an opportunity
        
        Args:
            opportunity_context: Dict containing:
                - budget: Opportunity budget
                - timeline: Timeline constraints
                - personas: List of decision makers
                - current_stage: Current sales stage
                - objections: List of known objections
                - competitive_landscape: Competitor information
                
        Returns:
            Recommended sales strategy with quantum optimization
        """
        try:
            logger.info(f"Navigating opportunity with context: {opportunity_context}")
            
            # 1) Build QUBO for path optimization
            qubo = self._build_path_qubo(opportunity_context)
            
            # 2) Solve with Dynex quantum optimization
            quantum_result = self.dynex.solve_qubo(qubo, {
                "agent": self.agent_id,
                "opportunity_id": opportunity_context.get("id", "unknown")
            })
            
            # 3) Generate strategic narrative with qdLLM
            strategy_prompt = self._build_strategy_prompt(opportunity_context, quantum_result)
            strategy_narrative = self.qdllm.generate(strategy_prompt, steps=8)
            
            # 4) Apply REVERSAL REASONINGâ„¢ to objections
            reversal_results = []
            for objection in opportunity_context.get("objections", []):
                reversal = self.qdllm.reason_reversal(
                    premise=f"Current objection: {objection}",
                    conclusion="Convert objection to opportunity",
                    objection=objection
                )
                reversal_results.append(reversal)
            
            # 5) Compile recommendation
            recommendation = {
                "agent": self.agent_id,
                "strategy": strategy_narrative,
                "quantum_optimization": quantum_result,
                "objection_reversals": reversal_results,
                "confidence_score": self._calculate_confidence(quantum_result),
                "next_steps": self._generate_next_steps(opportunity_context, quantum_result),
                "risk_factors": self._identify_risk_factors(opportunity_context),
                "success_probability": self._calculate_success_probability(quantum_result)
            }
            
            logger.info(f"Navigation complete with {recommendation['confidence_score']}% confidence")
            return recommendation
            
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return self._fallback_navigation(opportunity_context)
    
    def optimize_timing(self, opportunity_context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize timing for sales activities"""
        try:
            # Build timing QUBO considering multiple factors
            timing_qubo = self._build_timing_qubo(opportunity_context)
            timing_result = self.dynex.solve_qubo(timing_qubo, {"type": "timing_optimization"})
            
            return {
                "optimal_contact_times": timing_result.get("solution", {}).get("timing", []),
                "urgency_score": timing_result.get("solution", {}).get("urgency", 0.5),
                "next_best_action": self._determine_next_action(opportunity_context, timing_result)
            }
        except Exception as e:
            logger.error(f"Timing optimization failed: {e}")
            return {"error": "Timing optimization unavailable"}
    
    def predict_outcome(self, opportunity_context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict deal outcome with quantum probability modeling"""
        try:
            # Use hybrid inference for outcome prediction
            prediction_payload = {
                "context": opportunity_context,
                "historical_patterns": self._get_historical_patterns(),
                "market_conditions": self._get_market_conditions()
            }
            
            prediction_result = self.dynex.hybrid_inference("outcome_prediction", prediction_payload)
            
            return {
                "win_probability": prediction_result.get("result", {}).get("win_rate", 0.5),
                "expected_value": prediction_result.get("result", {}).get("expected_value", 0),
                "time_to_close": prediction_result.get("result", {}).get("time_to_close", 90),
                "key_risks": prediction_result.get("result", {}).get("risks", []),
                "recommended_actions": prediction_result.get("result", {}).get("actions", [])
            }
        except Exception as e:
            logger.error(f"Outcome prediction failed: {e}")
            return {"error": "Prediction unavailable"}
    
    def _build_path_qubo(self, context: Dict[str, Any]) -> Dict[Any, Any]:
        """Build QUBO for sales path optimization"""
        # Simplified QUBO considering budget, timeline, personas, and stage
        qubo = {}
        
        # Budget constraints
        budget = context.get("budget", 100000)
        qubo[(0, 0)] = -budget / 10000  # Higher budget = stronger bias
        
        # Timeline constraints  
        timeline = context.get("timeline", "Q4")
        timeline_urgency = {"Q1": 4, "Q2": 3, "Q3": 2, "Q4": 1}.get(timeline, 2)
        qubo[(1, 1)] = -timeline_urgency
        
        # Persona complexity
        personas = context.get("personas", [])
        qubo[(2, 2)] = -len(personas)  # More personas = more complex
        
        # Current stage progression
        stage = context.get("current_stage", "prospecting")
        stage_value = {"prospecting": 1, "qualification": 2, "proposal": 3, "negotiation": 4, "closing": 5}.get(stage, 1)
        qubo[(3, 3)] = -stage_value
        
        # Add interaction terms
        qubo[(0, 1)] = 0.5  # Budget-timeline interaction
        qubo[(2, 3)] = 0.3  # Personas-stage interaction
        
        return qubo
    
    def _build_strategy_prompt(self, context: Dict[str, Any], quantum_result: Dict[str, Any]) -> str:
        """Build prompt for strategic narrative generation"""
        return f"""
        Opportunity Context:
        - Budget: 
        - Timeline: {context.get('timeline', 'Unknown')}
        - Decision Makers: {', '.join(context.get('personas', []))}
        - Current Stage: {context.get('current_stage', 'Unknown')}
        - Known Objections: {', '.join(context.get('objections', []))}
        
        Quantum Optimization Result: {quantum_result}
        
        Generate a strategic sales narrative that leverages quantum insights to guide this opportunity to success.
        Focus on REVERSAL REASONINGâ„¢ to address objections and create compelling value propositions.
        """
    
    def _calculate_confidence(self, quantum_result: Dict[str, Any]) -> float:
        """Calculate confidence score from quantum result"""
        solution = quantum_result.get("solution", {})
        energy = abs(solution.get("energy", -10))
        return min(95.0, max(60.0, energy * 5))  # Convert energy to confidence percentage
    
    def _generate_next_steps(self, context: Dict[str, Any], quantum_result: Dict[str, Any]) -> List[str]:
        """Generate recommended next steps"""
        current_stage = context.get("current_stage", "prospecting")
        
        stage_steps = {
            "prospecting": [
                "Qualify budget authority and timeline",
                "Identify all decision makers and influencers", 
                "Map competitive landscape and differentiation"
            ],
            "qualification": [
                "Deep dive into pain points and business impact",
                "Quantify ROI and value proposition",
                "Schedule technical evaluation or demo"
            ],
            "proposal": [
                "Present tailored solution with ROI analysis",
                "Address anticipated objections proactively",
                "Set clear next steps and decision criteria"
            ],
            "negotiation": [
                "Focus on value-based pricing discussions",
                "Address final concerns and risk mitigation",
                "Prepare for contract and implementation planning"
            ],
            "closing": [
                "Finalize contract terms and legal review",
                "Coordinate implementation timeline and resources",
                "Ensure smooth transition and success planning"
            ]
        }
        
        return stage_steps.get(current_stage, ["Continue current approach"])
    
    def _identify_risk_factors(self, context: Dict[str, Any]) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        if context.get("budget", 0) < 50000:
            risks.append("Budget may be insufficient for full solution")
        
        if len(context.get("personas", [])) > 5:
            risks.append("Complex decision-making process with many stakeholders")
        
        if context.get("timeline") in ["Q4"]:
            risks.append("Year-end budget and timeline pressures")
        
        return risks
    
    def _calculate_success_probability(self, quantum_result: Dict[str, Any]) -> float:
        """Calculate success probability from quantum optimization"""
        confidence = self._calculate_confidence(quantum_result)
        return confidence * 0.8  # Convert confidence to success probability
    
    def _build_timing_qubo(self, context: Dict[str, Any]) -> Dict[Any, Any]:
        """Build QUBO for timing optimization"""
        return {
            (0, 0): -1,  # Immediate action bias
            (1, 1): -0.5,  # Follow-up timing
            (0, 1): 0.3  # Coordination between actions
        }
    
    def _determine_next_action(self, context: Dict[str, Any], timing_result: Dict[str, Any]) -> str:
        """Determine the next best action"""
        return "Schedule executive briefing with key stakeholders"
    
    def _get_historical_patterns(self) -> Dict[str, Any]:
        """Get historical sales patterns (mock data)"""
        return {
            "win_rate_by_stage": {
                "prospecting": 0.15,
                "qualification": 0.35,
                "proposal": 0.65,
                "negotiation": 0.85,
                "closing": 0.95
            },
            "avg_sales_cycle": 120,
            "common_objections": ["price", "timing", "competitor", "risk"]
        }
    
    def _get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions (mock data)"""
        return {
            "market_trend": "growing",
            "competition_level": "high",
            "budget_availability": "moderate",
            "urgency_level": "high"
        }
    
    def _fallback_navigation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback navigation when quantum processing fails"""
        return {
            "agent": self.agent_id,
            "strategy": "Classical sales approach recommended",
            "confidence_score": 70.0,
            "next_steps": ["Continue standard qualification process"],
            "risk_factors": ["Quantum optimization unavailable"],
            "success_probability": 56.0
        }
