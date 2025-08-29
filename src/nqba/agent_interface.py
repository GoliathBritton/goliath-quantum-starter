from typing import Any, Dict

class AgentInterface:
    """
    Abstract interface for Neuromorphic Quantum Business Architecture (NQBA) agents (business pods, quantum solvers, etc.)
    """
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}

    def run(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Agent must implement run() method.")

    def explain(self, *args, **kwargs) -> str:
        return f"Agent {self.name} executed with config: {self.config}"
