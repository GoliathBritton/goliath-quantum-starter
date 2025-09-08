#!/usr/bin/env python3
"""
Test script for quantum backend integration
"""

import asyncio
import json
from core.qsaiCore import QSAICore

async def test_quantum_integration():
    """Test quantum node processing with different operation types"""
    print("Testing Quantum Backend Integration...")
    
    # Initialize QSAICore
    core = QSAICore()
    
    # Test quantum optimization node
    optimization_step = {
        'id': 'quantum_opt_1',
        'name': 'Quantum Optimization Test',
        'type': 'quantum',
        'data': {
            'operation': 'optimization',
            'problem_type': 'qubo',
            'matrix': [[1, -1], [-1, 1]],
            'linear_terms': [0.5, -0.5],
            'num_reads': 100,
            'timeout': 30
        },
        'user_id': 'test_user'
    }
    
    print("\n1. Testing Quantum Optimization...")
    result = await core._process_quantum_node(optimization_step, {}, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test quantum simulation node
    simulation_step = {
        'id': 'quantum_sim_1',
        'name': 'Quantum Simulation Test',
        'type': 'quantum',
        'data': {
            'operation': 'simulation',
            'circuit': {'gates': ['H', 'CNOT'], 'qubits': 2},
            'shots': 1024
        }
    }
    
    print("\n2. Testing Quantum Simulation...")
    result = await core._process_quantum_node(simulation_step, {}, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test quantum machine learning node
    ml_step = {
        'id': 'quantum_ml_1',
        'name': 'Quantum ML Test',
        'type': 'quantum',
        'data': {
            'operation': 'machine_learning',
            'algorithm': 'qsvm',
            'training_data': [[1, 0], [0, 1], [1, 1], [0, 0]]
        }
    }
    
    print("\n3. Testing Quantum Machine Learning...")
    result = await core._process_quantum_node(ml_step, {}, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test unknown operation type
    unknown_step = {
        'id': 'quantum_unknown_1',
        'name': 'Unknown Operation Test',
        'type': 'quantum',
        'data': {
            'operation': 'unknown_operation'
        }
    }
    
    print("\n4. Testing Unknown Operation Type...")
    result = await core._process_quantum_node(unknown_step, {}, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n✅ Quantum Backend Integration Test Complete!")
    
    # Check if quantum hub is available
    if core.quantum_hub:
        print(f"\n🔬 Quantum Integration Hub Status: Available")
        print(f"   Hub Type: {type(core.quantum_hub).__name__}")
    else:
        print(f"\n⚠️  Quantum Integration Hub Status: Not Available (using fallback)")

if __name__ == "__main__":
    asyncio.run(test_quantum_integration())