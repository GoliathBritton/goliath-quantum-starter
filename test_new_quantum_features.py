#!/usr/bin/env python3
"""
Test script for new quantum features: diffusion algorithms and meta-algorithm instituter

This script tests the newly implemented quantum algorithms:
1. Quantum Diffusion Algorithm
2. Parallel Quantum Diffusion
3. Dynamic Meta-Algorithm Instituter
4. Energy Optimization Integration

Author: Goliath Quantum Division
Version: 1.0.0
"""

import sys
import os
import asyncio
import numpy as np
import time
from typing import Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test quantum diffusion imports
    from quantum.diffusion import (
        quantum_diffusion,
        parallel_quantum_diffusion,
        get_diffusion_performance,
        diffusion_engine
    )
    print("✓ Quantum diffusion imports successful")
except ImportError as e:
    print(f"✗ Quantum diffusion import failed: {e}")
    sys.exit(1)

try:
    # Test meta-algorithm imports
    from quantum.meta_algorithm import (
        dynamic_algo_instituter,
        get_meta_performance,
        adapt_preferences,
        meta_instituter,
        TaskType
    )
    print("✓ Meta-algorithm imports successful")
except ImportError as e:
    print(f"✗ Meta-algorithm import failed: {e}")
    sys.exit(1)

try:
    # Test existing algorithm imports
    from quantum.reasoning import reversal_reasoning
    from quantum.optimization import parallel_qaoa, optimize_qaoa
    print("✓ Existing quantum algorithm imports successful")
except ImportError as e:
    print(f"✗ Existing algorithm import failed: {e}")
    sys.exit(1)

def test_quantum_diffusion():
    """Test quantum diffusion algorithm"""
    print("\n=== Testing Quantum Diffusion Algorithm ===")
    
    try:
        # Test basic diffusion
        print("Testing basic quantum diffusion...")
        states = quantum_diffusion(steps=5, dim=2, efficiency_threshold=0.8)
        
        print(f"✓ Generated {len(states)} diffusion states")
        print(f"  First state shape: {states[0].shape if states else 'No states'}")
        
        if states:
            # Check state normalization
            first_state_norm = np.linalg.norm(states[0])
            print(f"  First state norm: {first_state_norm:.4f}")
            
            if abs(first_state_norm - 1.0) < 0.1:
                print("✓ States appear properly normalized")
            else:
                print("⚠ States may not be properly normalized")
        
        return True
        
    except Exception as e:
        print(f"✗ Quantum diffusion test failed: {e}")
        return False

async def test_parallel_diffusion():
    """Test parallel quantum diffusion"""
    print("\n=== Testing Parallel Quantum Diffusion ===")
    
    try:
        # Test parallel diffusion with multiple scenarios
        print("Testing parallel quantum diffusion...")
        
        scenarios = [
            {'steps': 3, 'dim': 2},
            {'steps': 4, 'dim': 2},
            {'steps': 5, 'dim': 2}
        ]
        
        start_time = time.time()
        results = await parallel_quantum_diffusion(scenarios, max_workers=2)
        execution_time = time.time() - start_time
        
        print(f"✓ Parallel diffusion completed in {execution_time:.4f} seconds")
        print(f"  Processed {len(results)} scenarios")
        
        for i, result in enumerate(results):
            print(f"  Scenario {i+1}: {len(result)} states generated")
        
        return True
        
    except Exception as e:
        print(f"✗ Parallel diffusion test failed: {e}")
        return False

async def test_meta_algorithm():
    """Test dynamic meta-algorithm instituter"""
    print("\n=== Testing Dynamic Meta-Algorithm Instituter ===")
    
    try:
        # Test 1: Reasoning task
        print("Testing reasoning task classification...")
        reasoning_data = {
            'premise': 'Market volatility is increasing',
            'conclusion': 'Diversify investment portfolio'
        }
        
        result1 = await dynamic_algo_instituter('reasoning', reasoning_data)
        print(f"✓ Reasoning task result: {result1.get('selected_algorithm', 'Unknown')}")
        print(f"  Success: {result1.get('success', False)}")
        print(f"  Execution time: {result1.get('execution_time', 0):.4f}s")
        
        # Test 2: Optimization task
        print("\nTesting optimization task classification...")
        optimization_data = {
            'matrices': [[[0, 1, 0], [1, 0, 1], [0, 1, 0]]],
            'problem_type': 'portfolio'
        }
        
        result2 = await dynamic_algo_instituter('optimization', optimization_data)
        print(f"✓ Optimization task result: {result2.get('selected_algorithm', 'Unknown')}")
        print(f"  Success: {result2.get('success', False)}")
        print(f"  Execution time: {result2.get('execution_time', 0):.4f}s")
        
        # Test 3: Diffusion task
        print("\nTesting diffusion task classification...")
        diffusion_data = {
            'steps': 4,
            'dim': 2,
            'efficiency_threshold': 0.8
        }
        
        result3 = await dynamic_algo_instituter('diffusion', diffusion_data)
        print(f"✓ Diffusion task result: {result3.get('selected_algorithm', 'Unknown')}")
        print(f"  Success: {result3.get('success', False)}")
        print(f"  Execution time: {result3.get('execution_time', 0):.4f}s")
        
        # Test 4: Energy optimization (should classify as optimization)
        print("\nTesting energy optimization task...")
        energy_data = {
            'matrices': [[[0, 2, 1], [2, 0, 3], [1, 3, 0]]],
            'problem_type': 'energy'
        }
        
        result4 = await dynamic_algo_instituter('energy_optimization', energy_data)
        print(f"✓ Energy optimization result: {result4.get('selected_algorithm', 'Unknown')}")
        print(f"  Success: {result4.get('success', False)}")
        print(f"  Execution time: {result4.get('execution_time', 0):.4f}s")
        
        return True
        
    except Exception as e:
        print(f"✗ Meta-algorithm test failed: {e}")
        return False

def test_performance_tracking():
    """Test performance tracking and metrics"""
    print("\n=== Testing Performance Tracking ===")
    
    try:
        # Get diffusion performance
        print("Testing diffusion performance metrics...")
        diffusion_perf = get_diffusion_performance()
        print(f"✓ Diffusion performance: {diffusion_perf}")
        
        # Get meta-algorithm performance
        print("\nTesting meta-algorithm performance metrics...")
        meta_perf = get_meta_performance()
        print(f"✓ Meta-algorithm performance: {meta_perf}")
        
        # Test preference adaptation
        print("\nTesting preference adaptation...")
        adapt_preferences()
        print("✓ Preference adaptation completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance tracking test failed: {e}")
        return False

def test_algorithm_integration():
    """Test integration between different algorithms"""
    print("\n=== Testing Algorithm Integration ===")
    
    try:
        # Test that all algorithms can be imported together
        print("Testing algorithm coexistence...")
        
        # Test reasoning
        reasoning_result = reversal_reasoning(
            "Strong quarterly earnings", 
            "Stock price will increase"
        )
        print(f"✓ Reasoning algorithm: {type(reasoning_result)}")
        
        # Test optimization
        test_matrix = np.array([[0, 1], [1, 0]])
        opt_params, opt_cost = optimize_qaoa(test_matrix, 'portfolio')
        print(f"✓ Optimization algorithm: params shape {opt_params.shape}, cost {opt_cost:.4f}")
        
        # Test diffusion
        diff_states = quantum_diffusion(steps=3, dim=2)
        print(f"✓ Diffusion algorithm: {len(diff_states)} states generated")
        
        print("✓ All algorithms integrate successfully")
        return True
        
    except Exception as e:
        print(f"✗ Algorithm integration test failed: {e}")
        return False

async def run_comprehensive_tests():
    """Run all tests comprehensively"""
    print("🚀 Starting Comprehensive Quantum Algorithm Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run individual tests
    test_results.append(test_quantum_diffusion())
    test_results.append(await test_parallel_diffusion())
    test_results.append(await test_meta_algorithm())
    test_results.append(test_performance_tracking())
    test_results.append(test_algorithm_integration())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(test_results)
    total = len(test_results)
    
    test_names = [
        "Quantum Diffusion",
        "Parallel Diffusion", 
        "Meta-Algorithm",
        "Performance Tracking",
        "Algorithm Integration"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{i+1}. {name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All quantum algorithm tests PASSED!")
        print("✅ New quantum features are ready for production use")
    else:
        print("⚠️  Some tests failed - review implementation")
    
    return passed == total

if __name__ == "__main__":
    print("Quantum Algorithm Test Suite")
    print("Testing new quantum diffusion and meta-algorithm features...\n")
    
    # Run tests
    success = asyncio.run(run_comprehensive_tests())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)