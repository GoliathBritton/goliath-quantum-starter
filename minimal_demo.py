#!/usr/bin/env python3
"""
FLYFOX AI: Minimal Quantum Platform Demo
"""

import sys
import os
import asyncio

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

async def main():
    """Run a minimal demo."""
    print(" FLYFOX AI: Minimal Quantum Platform Demo")
    print("=" * 50)
    
    print("\n1. Testing basic Python...")
    try:
        import numpy as np
        print(" ✓ NumPy imported successfully")
        
        # Test basic numpy operations
        arr = np.array([1, 2, 3, 4])
        print(f"   Test array: {arr}")
        print(f"   Array sum: {np.sum(arr)}")
        
    except Exception as e:
        print(f" ✗ NumPy test failed: {e}")
        return 1
    
    print("\n2. Testing basic imports...")
    try:
        # Test importing basic modules
        import nqba.engine
        print(" ✓ NQBA engine imported successfully")
        
        import nqba.quantum_adapter
        print(" ✓ Quantum adapter imported successfully")
        
        import nqba.decision_logic
        print(" ✓ Decision logic imported successfully")
        
    except Exception as e:
        print(f" ✗ Basic imports failed: {e}")
        return 1
    
    print("\n3. Testing quantum components...")
    try:
        import goliath.quantum.sigmaeq_engine
        print(" ✓ SigmaEQ engine imported successfully")
        
        import goliath.quantum.dynex_integration
        print(" ✓ Dynex integration imported successfully")
        
    except Exception as e:
        print(f" ✗ Quantum components failed: {e}")
        return 1
    
    print("\n4. Testing main interface...")
    try:
        import goliath.quantum.goliath_quantum
        print(" ✓ Goliath Quantum imported successfully")
        
    except Exception as e:
        print(f" ✗ Main interface failed: {e}")
        return 1
    
    print("\n5. Testing basic functionality...")
    try:
        from goliath.quantum.goliath_quantum import GoliathQuantum
        
        # Initialize with minimal settings
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=False,
            max_qubits=8,
            enable_dynex=False
        )
        print(" ✓ GoliathQuantum initialized successfully")
        
        # Test basic methods
        algorithms = client.get_supported_algorithms()
        print(f"   Supported algorithms: {len(algorithms)} found")
        
        # Clean up
        await client.close()
        print(" ✓ Cleanup completed")
        
    except Exception as e:
        print(f" ✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 50)
    print(" Minimal demo completed successfully!")
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
