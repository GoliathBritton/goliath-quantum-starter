from .agent_interface import AgentInterface
from .decision_logic import decide
from .quantum_adapter import optimize_qubo
from .ltc_logger import ltc_record


class LeadScoringPod(AgentInterface):
    """Business pod for quantum/AI-powered lead scoring."""

    def run(self, features: dict, policy_id: str = "lead_score_v1"):
        result = decide(policy_id, features)
        ltc = ltc_record(
            policy_id=policy_id,
            inputs={"features": features},
            outputs=result["result"],
            explanation=result["explanation"],
            solver_backend="decision.logic",
        )
        return {"decision": result, "ltc": ltc}


class QuantumOptimizerPod(AgentInterface):
    """Business pod for quantum optimization (QUBO, etc.)."""

    def run(
        self,
        variables: int,
        Q: list,
        constraints: list = None,
        objective: str = "maximize",
    ):
        result = optimize_qubo(variables, Q, constraints, objective)
        ltc = ltc_record(
            policy_id="optimize.qubo",
            inputs={"variables": variables, "Q": Q, "constraints": constraints},
            outputs={
                "assignment": result["assignment"],
                "objective_value": result["objective_value"],
            },
            explanation="QUBO optimization via pod",
            solver_backend=result["backend"],
        )
        return {"optimization": result, "ltc": ltc}


# Recommendation: Add more pods for sales scripting, energy optimization, insurance quoting, etc.
# Example stub:
class SalesScriptPod(AgentInterface):
    def run(self, context: dict):
        # Placeholder: generate a sales script using context
        script = f"Hello, {context.get('name', 'Customer')}! This is your quantum-personalized script."
        ltc = ltc_record(
            policy_id="sales.script.v1",
            inputs=context,
            outputs={"script": script},
            explanation="Generated sales script",
            solver_backend="script.logic",
        )
        return {"script": script, "ltc": ltc}
