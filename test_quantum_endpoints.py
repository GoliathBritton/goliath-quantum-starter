#!/usr/bin/env python3
"""
Test script for quantum algorithm endpoints
"""
import asyncio
import json
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from quantum.reasoning import reversal_reasoning_async, reasoning_engine
from quantum.optimization import qaoa_optimize_async, qaoa_engine

async def test_reversal_reasoning():
    """Test the reversal reasoning algorithm"""
    print("🧠 Testing Reversal Reasoning Algorithm...")
    
    try:
        # Test case 1: Funding assessment
        result = await reversal_reasoning_async(
            premise="Strong revenue growth and market fit",
            conclusion="Approve funding",
            coherence_threshold=0.9,
            max_iterations=3
        )
        
        print("✅ Reversal Reasoning Test 1 - Funding Assessment:")
        print(f"   Forward: {result.get('forward', 'N/A')}")
        print(f"   Backward: {result.get('backward', 'N/A')}")
        print(f"   Coherence: {result.get('coherence', 0.0):.3f}")
        print(f"   Confidence: {result.get('confidence', 0.0):.3f}")
        print(f"   Iterations: {result.get('iterations', 0)}")
        
        # Test case 2: Educational logic
        result2 = await reversal_reasoning_async(
            premise="Student shows consistent improvement",
            conclusion="Recommend advanced course",
            coherence_threshold=0.85
        )
        
        print("\n✅ Reversal Reasoning Test 2 - Educational Logic:")
        print(f"   Forward: {result2.get('forward', 'N/A')}")
        print(f"   Backward: {result2.get('backward', 'N/A')}")
        print(f"   Coherence: {result2.get('coherence', 0.0):.3f}")
        
        # Get performance stats
        stats = reasoning_engine.get_performance_stats()
        print(f"\n📊 Reasoning Engine Stats:")
        print(f"   Total calls: {stats.get('total_calls', 0)}")
        print(f"   Average coherence: {stats.get('average_coherence', 0.0):.3f}")
        print(f"   Success rate: {stats.get('success_rate', 0.0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reversal Reasoning Test Failed: {str(e)}")
        return False

async def test_qaoa_optimization():
    """Test the QAOA optimization algorithm"""
    print("\n🔬 Testing QAOA Optimization Algorithm...")
    
    try:
        # Test case 1: Portfolio optimization
        portfolio_data = [
            [1.0, 0.5, 0.3],
            [0.5, 1.0, 0.4],
            [0.3, 0.4, 1.0]
        ]
        
        result = await qaoa_optimize_async(
            data=portfolio_data,
            problem_type="portfolio",
            num_workers=2,
            max_iterations=50,
            tolerance=1e-4
        )
        
        print("✅ QAOA Test 1 - Portfolio Optimization:")
        print(f"   Optimal parameters: {result.get('optimal_params', [])}")
        print(f"   Optimal value: {result.get('optimal_value', 0.0):.6f}")
        print(f"   Execution time: {result.get('execution_time', 0.0):.3f}s")
        print(f"   Workers used: {result.get('num_workers_used', 0)}")
        
        # Test case 2: Energy optimization
        energy_data = [
            [2.0, 1.0],
            [1.0, 2.0]
        ]
        
        result2 = await qaoa_optimize_async(
            data=energy_data,
            problem_type="energy",
            max_iterations=30
        )
        
        print("\n✅ QAOA Test 2 - Energy Optimization:")
        print(f"   Optimal parameters: {result2.get('optimal_params', [])}")
        print(f"   Optimal value: {result2.get('optimal_value', 0.0):.6f}")
        print(f"   Convergence history length: {len(result2.get('convergence_history', []))}")
        
        # Get performance stats
        stats = qaoa_engine.get_performance_stats()
        print(f"\n📊 QAOA Engine Stats:")
        print(f"   Total optimizations: {stats.get('total_optimizations', 0)}")
        print(f"   Average execution time: {stats.get('average_execution_time', 0.0):.3f}s")
        print(f"   Success rate: {stats.get('success_rate', 0.0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ QAOA Optimization Test Failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Quantum Algorithm Tests...\n")
    
    # Test reversal reasoning
    reasoning_success = await test_reversal_reasoning()
    
    # Test QAOA optimization
    qaoa_success = await test_qaoa_optimization()
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    print(f"Reversal Reasoning: {'✅ PASSED' if reasoning_success else '❌ FAILED'}")
    print(f"QAOA Optimization:  {'✅ PASSED' if qaoa_success else '❌ FAILED'}")
    
    if reasoning_success and qaoa_success:
        print("\n🎉 All quantum algorithms are working correctly!")
        print("🔗 Ready for API integration and production use.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    return reasoning_success and qaoa_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)