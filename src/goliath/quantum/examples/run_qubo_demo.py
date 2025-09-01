#!/usr/bin/env python3
"""
FLYFOX AI: Quantum Computing Platform Demo Script

This script demonstrates the FLYFOX AI Quantum Computing Platform with simulator mode.
Run this to test the basic functionality before deploying to production.
"""

import sys
import os
import asyncio
import numpy as np

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from goliath.quantum.goliath_quantum import GoliathQuantum

async def main():
    """Run the FLYFOX AI Quantum demo."""
    print(" FLYFOX AI: Quantum Computing Platform Demo")
    print("=" * 50)
    
    # Initialize with simulator mode (safe for testing)
    print("\n1. Initializing FLYFOX AI Quantum Platform in simulator mode...")
    client = GoliathQuantum(
        use_simulator=True,  # Safe for testing
        apollo_mode=True,     # Enable Apollo emulation
        qdllm_params=400_000_000_000,  # 400B parameters
        max_qubits=32,        # Limit for demo
        enable_dynex=False    # Disable for demo (no API key)
    )
    print(" ✓ Initialized successfully")
    
    # Test QUBO optimization
    print("\n2. Testing QUBO optimization...")
    qubo_matrix = np.array([
        [1, -1, 0, 0],
        [-1, 2, -1, 0],
        [0, -1, 3, -1],
        [0, 0, -1, 4]
    ])
    
    try:
        result = await client.optimize_qubo(
            qubo_matrix=qubo_matrix,
            algorithm="qaoa",
            enable_pouw=False  # Disable for demo
        )
        
        if result.success:
            print(" ✓ QUBO optimization successful!")
            print(f"   Solution: {result.solution}")
            print(f"   Optimal Value: {result.optimal_value:.4f}")
            print(f"   Execution Time: {result.execution_time:.3f}s")
            print(f"   Algorithm: {result.metadata.get('algorithm', 'N/A')}")
        else:
            print(f" ✗ QUBO optimization failed: {result.error_message}")
            
    except Exception as e:
        print(f" ✗ QUBO optimization failed: {e}")
    
    # Test quantum ML
    print("\n3. Testing Quantum Machine Learning...")
    # Create sample data
    X = np.random.randn(100, 4)  # 100 samples, 4 features
    y = np.random.randint(0, 2, 100)  # Binary labels
    
    try:
        ml_result = await client.run_quantum_ml(
            data=X,
            algorithm="qsvm",
            enable_pouw=False
        )
        
        if ml_result.success:
            print(" ✓ Quantum ML successful!")
            print(f"   Data Shape: {X.shape}")
            print(f"   Algorithm: {ml_result.metadata.get('algorithm', 'N/A')}")
            print(f"   Execution Time: {ml_result.execution_time:.3f}s")
        else:
            print(f" ✗ Quantum ML failed: {ml_result.error_message}")
            
    except Exception as e:
        print(f" ✗ Quantum ML failed: {e}")
    
    # Test quantum circuit execution
    print("\n4. Testing Quantum Circuit Execution...")
    circuit_spec = {
        "qubits": 4,
        "gates": [
            {"type": "h", "target": 0},
            {"type": "h", "target": 1},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "h", "target": 2},
            {"type": "cx", "control": 1, "target": 2},
            {"type": "h", "target": 3},
            {"type": "cx", "control": 2, "target": 3}
        ],
        "measurements": [0, 1, 2, 3]
    }
    
    try:
        circuit_result = await client.execute_quantum_circuit(circuit_spec, optimization_level=2)
        
        if circuit_result["success"]:
            print(" ✓ Circuit execution successful!")
            print(f"   Qubits: {circuit_spec['qubits']}")
            print(f"   Gates: {len(circuit_spec['gates'])}")
            print(f"   Execution Time: {circuit_result['execution_time']:.3f}s")
            print(f"   Backend: {circuit_result['result_data'].get('backend', 'N/A')}")
        else:
            print(f" ✗ Circuit execution failed: {circuit_result['error_message']}")
            
    except Exception as e:
        print(f" ✗ Circuit execution failed: {e}")
    
    # Get system statistics
    print("\n5. System Statistics...")
    try:
        stats = client.get_optimization_statistics()
        print(f"   Total Optimizations: {stats['total_optimizations']}")
        print(f"   Success Rate: {stats['success_rate']:.2%}")
        print(f"   Execution Mode: {stats['execution_mode']}")
        print(f"   Max Qubits: {stats['max_qubits']}")
        print(f"   Apollo Mode: {stats['apollo_mode']}")
        
        # NQBA Engine stats
        nqba_stats = stats['nqba_engine']
        print(f"   NQBA Executions: {nqba_stats['total_executions']}")
        print(f"   NQBA Success Rate: {nqba_stats['success_rate']:.2%}")
        
        # SigmaEQ Engine stats
        sigmaeq_stats = stats['sigmaeq_engine']
        print(f"   SigmaEQ Optimizations: {sigmaeq_stats['total_optimizations']}")
        print(f"   SigmaEQ Success Rate: {sigmaeq_stats['success_rate']:.2%}")
        
    except Exception as e:
        print(f" ✗ Failed to get statistics: {e}")
    
    # Get supported algorithms
    print("\n6. Supported Algorithms...")
    try:
        algorithms = client.get_supported_algorithms()
        print("   Supported optimization algorithms:")
        for alg in algorithms:
            print(f"     - {alg}")
    except Exception as e:
        print(f" ✗ Failed to get algorithms: {e}")
    
    # Test Dynex integration (if enabled)
    if client.enable_dynex:
        print("\n7. Dynex Integration Test...")
        try:
            network_status = await client.get_network_status()
            if network_status.get("connected"):
                print("   ✓ Connected to Dynex network")
                print(f"   Network: {network_status.get('network', 'N/A')}")
                print(f"   Block Height: {network_status.get('block_height', 'N/A')}")
            else:
                print("   ✗ Not connected to Dynex network")
                
        except Exception as e:
            print(f"   ✗ Dynex test failed: {e}")
    else:
        print("\n7. Dynex Integration: Disabled for demo")
    
    print("\n" + "=" * 50)
    print(" Demo completed successfully!")
    
    # Clean up
    await client.close()
    
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
        sys.exit(1)
