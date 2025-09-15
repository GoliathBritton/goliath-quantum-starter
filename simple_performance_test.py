"""Simple test to validate performance tracking functionality."""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from nqba_stack.algorithms.performance_engine import (
        PerformanceTracker,
        PerformanceMetrics,
        performance_engine
    )
    from nqba_stack.algorithms.quantum_enhanced_algorithms import (
        AlgorithmType,
        AlgorithmResult,
        QuantumAlgorithmFactory
    )
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_performance_tracker():
    """Test basic performance tracking functionality."""
    print("\n=== Testing Performance Tracker ===")
    
    tracker = PerformanceTracker()
    
    # Create test metrics
    metrics = PerformanceMetrics(
        execution_time=1.5,
        memory_usage=512.0,
        cpu_utilization=75.0,
        quantum_gate_count=100,
        circuit_depth=20,
        fidelity=0.95,
        success_rate=0.98
    )
    
    # Record performance
    tracker.record_performance(
        algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
        metrics=metrics,
        context={"problem_size": 10}
    )
    
    # Get history
    history = tracker.get_performance_history(AlgorithmType.PORTFOLIO_OPTIMIZATION)
    
    if len(history) == 1:
        print("✓ Performance recording works")
        print(f"  - Execution time: {history[0].metrics.execution_time}s")
        print(f"  - Memory usage: {history[0].metrics.memory_usage}MB")
        print(f"  - Problem size: {history[0].context['problem_size']}")
    else:
        print("✗ Performance recording failed")
        return False
    
    return True

async def test_algorithm_with_tracking():
    """Test algorithm execution with performance tracking."""
    print("\n=== Testing Algorithm with Performance Tracking ===")
    
    try:
        factory = QuantumAlgorithmFactory()
        algorithm = factory.create_algorithm(AlgorithmType.PORTFOLIO_OPTIMIZATION)
        
        # Test data
        returns_data = [[0.1, 0.05, 0.08], [0.02, 0.15, 0.03], [0.08, 0.01, 0.12]]
        risk_tolerance = 0.5
        
        # Run algorithm
        result = await algorithm.optimize_portfolio(
            returns_data=returns_data,
            risk_tolerance=risk_tolerance
        )
        
        if hasattr(result, 'performance_metrics') and result.performance_metrics:
            print("✓ Algorithm performance tracking works")
            print(f"  - Execution time: {result.performance_metrics.execution_time:.3f}s")
            print(f"  - Memory usage: {result.performance_metrics.memory_usage:.1f}MB")
            print(f"  - CPU utilization: {result.performance_metrics.cpu_utilization:.1f}%")
            return True
        else:
            print("✗ Algorithm performance tracking failed")
            return False
            
    except Exception as e:
        print(f"✗ Algorithm test failed: {e}")
        return False

def test_global_performance_engine():
    """Test the global performance engine instance."""
    print("\n=== Testing Global Performance Engine ===")
    
    try:
        # Test that global instance exists
        if performance_engine.performance_tracker:
            print("✓ Global performance engine initialized")
            
            # Test recording through global instance
            metrics = PerformanceMetrics(
                execution_time=0.8,
                memory_usage=256.0,
                cpu_utilization=60.0,
                quantum_gate_count=50,
                circuit_depth=10,
                fidelity=0.92,
                success_rate=0.96
            )
            
            performance_engine.performance_tracker.record_performance(
                algorithm_type=AlgorithmType.ENERGY_MANAGEMENT,
                metrics=metrics,
                context={"grid_size": 5}
            )
            
            history = performance_engine.performance_tracker.get_performance_history(
                AlgorithmType.ENERGY_MANAGEMENT
            )
            
            if len(history) >= 1:
                print("✓ Global performance engine recording works")
                return True
            else:
                print("✗ Global performance engine recording failed")
                return False
        else:
            print("✗ Global performance engine not initialized")
            return False
            
    except Exception as e:
        print(f"✗ Global performance engine test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Starting Performance Engine Validation Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Basic performance tracker
    if test_performance_tracker():
        tests_passed += 1
    
    # Test 2: Algorithm with tracking
    if await test_algorithm_with_tracking():
        tests_passed += 1
    
    # Test 3: Global performance engine
    if test_global_performance_engine():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Performance tracking system is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)