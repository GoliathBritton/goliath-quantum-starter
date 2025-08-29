"""
USAGE EXAMPLES for MCP API and Handler
--------------------------------------
- Shows how to call the API endpoints and handler directly
- Includes real backend logic stub for QUBO optimization
"""

import asyncio
import httpx
from nqba_stack import mcp_handler


# Example: Direct handler call (Python)
async def example_direct_qubo():
    payload = {
        "qubo_matrix": [[1, -1], [-1, 2]],
        "linear_terms": [0.5, -0.5],
        "constraints": {},
        "preferred_provider": "dynex",
        "max_runtime": 10,
    }
    result = await mcp_handler.dispatch_tool(
        "quantum.optimize.qubo", payload, user="demo"
    )
    print("Direct handler result:", result)


# Example: HTTP API call (requests)
async def example_api_qubo():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/tools/quantum.optimize.qubo",
            json={
                "payload": {
                    "qubo_matrix": [[1, -1], [-1, 2]],
                    "linear_terms": [0.5, -0.5],
                    "constraints": {},
                    "preferred_provider": "dynex",
                    "max_runtime": 10,
                },
                "user": "demo",
            },
        )
        print("API result:", resp.json())


# Example: Real backend logic stub (replace in mcp_handler)
# In mcp_handler.py, inside handle_optimize_qubo:
# from nqba_stack.engine import NQBAEngine, ExecutionMode
# nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
# result = await nqba.optimize_qubo(payload)
# return result

if __name__ == "__main__":
    asyncio.run(example_direct_qubo())
    # asyncio.run(example_api_qubo())  # Uncomment if API server is running
