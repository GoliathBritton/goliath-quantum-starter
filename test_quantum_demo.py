#!/usr/bin/env python3
"""
Simple test script to verify quantum algorithms are working
"""
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("🚀 Starting Quantum Algorithms Test...")
print("=" * 50)

try:
    from nqba_stack.algorithms.runner import (
        run_algorithm,
        AlgorithmType,
        AlgorithmConfig,
        BackendType
    )
    print("✅ Successfully imported quantum algorithms")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

async def test_quantum_classifier():
    """Test the quantum classifier"""
    print("\n🧠 Testing Quantum Classifier...")
    
    try:
        config = AlgorithmConfig(
            algorithm_type=AlgorithmType.QUANTUM_CLASSIFIER,
            backend_type=BackendType.SIMULATOR,
            parameters={
                "dataset": "synthetic",
                "num_samples": 100,
                "num_features": 4,
                "num_classes": 2,
                "num_layers": 2,
                "feature_map_type": "ZZFeatureMap",
                "ansatz_type": "RealAmplitudes",
                "optimizer": "COBYLA",
                "max_iter": 50
            }
        )
        
        result = await run_algorithm(config, {})
        
        if result.get("success"):
            print(f"✅ Quantum Classifier completed successfully!")
            print(f"   Accuracy: {result.get('accuracy', 'N/A')}")
            print(f"   Training time: {result.get('training_time', 'N/A')}s")
            return True
        else:
            print(f"❌ Quantum Classifier failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Quantum Classifier test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("\n🔬 Running Quantum Algorithm Tests...")
    
    # Test quantum classifier
    classifier_success = await test_quantum_classifier()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    
    if classifier_success:
        print("✅ All tests passed! Quantum algorithms are working.")
        print("\n🎉 The quantum computing stack is ready for deployment!")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    print("\n🚀 Test completed.")

if __name__ == "__main__":
    asyncio.run(main())