#!/usr/bin/env python3
"""
FLYFOX AI: Goliath Quantum Demo Script

This script demonstrates the GoliathQuantum module with simulator mode.
Run this to test the basic functionality before deploying to production.
"""

import sys
import os

# Add the parent directory to the path so we can import goliath_quantum
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from goliath.quantum import GoliathQuantum

def main():
    """Run the Goliath Quantum demo."""
    print(" FLYFOX AI: Goliath Quantum Demo")
    print("=" * 50)
    
    # Initialize with simulator mode (safe for testing)
    print("\n1. Initializing GoliathQuantum in simulator mode...")
    client = GoliathQuantum(
        use_simulator=True,  # Safe for testing
        apollo_mode=True,     # Enable Apollo emulation
        qdllm_params=400_000_000_000  # 400B parameters
    )
    print(" Initialized successfully")
    
    # Test QUBO optimization
    print("\n2. Testing QUBO optimization...")
    qubo_problem = {
        "qubo_matrix": [[1, -1], [-1, 2]], 
        "meta": {"purpose": "demo", "description": "Simple 2x2 QUBO test"}
    }
    
    try:
        result = client.optimize(qubo_problem)
        print(" QUBO optimization successful!")
        print(f"   Solution: {result.get(\"solution_bits\", \"N/A\")}")
        print(f"   Score: {result.get(\"score\", \"N/A\")}")
        print(f"   Apollo mode: {result.get(\"apollo_mode\", False)}")
        
        if \"pouw_receipt\" in result:
            receipt = result[\"pouw_receipt\"]
            print(f"   PoUW receipt: {receipt.get(\"green_credits\", 0)} green credits")
            
    except Exception as e:
        print(f" QUBO optimization failed: {e}")
    
    print("\n" + "=" * 50)
    print(" Demo completed successfully!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
