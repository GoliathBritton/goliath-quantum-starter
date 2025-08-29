"""
NQBA Engine: Core orchestration and execution layer for modular business agents.
Handles agent registration, task routing, and API integration.
"""

from typing import Dict, Any, Callable


class NQBAEngine:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name: str, agent: Callable):
        self.agents[name] = agent

    def run(self, agent_name: str, *args, **kwargs) -> Any:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not registered.")
        return self.agents[agent_name](*args, **kwargs)


# Example usage:
# engine = NQBAEngine()
# engine.register_agent('sigmaeq', sigmaeq_agent)
# result = engine.run('sigmaeq', input_data)
