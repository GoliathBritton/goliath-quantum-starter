#!/usr/bin/env python3
"""
FLYFOX AI: Simple Quantum Platform Demo
"""

import sys
import os
import asyncio
import numpy as np

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

async def main():
    """Run a simple demo."""
    print(" FLYFOX AI: Simple Quantum Platform Demo")
    print("=" * 50)
    
    print("\n1. Testing basic imports...")
    try:
        # Test basic imports
        import nqba.engine
        print(" ✓ NQBA engine imported successfully")
        
        import nqba.quantum_adapter
        print(" ✓ Quantum adapter imported successfully")
        
        import nqba.decision_logic
        print(" ✓ Decision logic imported successfully")
        
        import goliath.quantum.sigmaeq_engine
        print(" ✓ SigmaEQ engine imported successfully")
        
        import goliath.quantum.dynex_integration
        print(" ✓ Dynex integration imported successfully")
        
        import goliath.quantum.goliath_quantum
        print(" ✓ Goliath Quantum imported successfully")
        
    except Exception as e:
        print(f" ✗ Import failed: {e}")
        return 1
    
    print("\n2. Testing basic functionality...")
    try:
        from goliath.quantum.goliath_quantum import GoliathQuantum
        
        # Initialize with simulator mode
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=True,
            max_qubits=16,
            enable_dynex=False
        )
        print(" ✓ GoliathQuantum initialized successfully")
        
        # Test basic methods
        algorithms = client.get_supported_algorithms()
        print(f" ✓ Supported algorithms: {len(algorithms)} found")
        
        stats = client.get_optimization_statistics()
        print(f" ✓ Statistics retrieved: {stats['total_optimizations']} optimizations")
        
        # Clean up
        await client.close()
        print(" ✓ Cleanup completed")
        
    except Exception as e:
        print(f" ✗ Functionality test failed: {e}")
        return 1
    
    print("\n" + "=" * 50)
    print(" Simple demo completed successfully!")
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
