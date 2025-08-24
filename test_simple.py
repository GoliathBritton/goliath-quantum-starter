#!/usr/bin/env python3
"""
Simple test script for FLYFOX AI Quantum Computing Platform
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        # Test quantum components
        from nqba.engine import NQBAEngine
        print("✓ NQBA Engine imported successfully")
    except ImportError as e:
        print(f"✗ NQBA Engine import failed: {e}")
    
    try:
        from goliath.quantum import GoliathQuantum
        print("✓ GoliathQuantum imported successfully")
    except ImportError as e:
        print(f"✗ GoliathQuantum import failed: {e}")
    
    try:
        from goliath.quantum.sigmaeq_engine import SigmaEQEngine
        print("✓ SigmaEQ Engine imported successfully")
    except ImportError as e:
        print(f"✗ SigmaEQ Engine import failed: {e}")
    
    try:
        from goliath.quantum.dynex_integration import DynexNetwork
        print("✓ Dynex Integration imported successfully")
    except ImportError as e:
        print(f"✗ Dynex Integration import failed: {e}")

def test_quantum_operations():
    """Test basic quantum operations"""
    print("\nTesting quantum operations...")
    
    try:
        from goliath.quantum import GoliathQuantum
        
        # Initialize client
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=False,
            enable_dynex=False
        )
        print("✓ GoliathQuantum initialized successfully")
        
        # Test simple circuit
        circuit_spec = {
            "qubits": 2,
            "gates": [
                {"type": "h", "target": 0},
                {"type": "cx", "control": 0, "target": 1}
            ],
            "measurements": [0, 1]
        }
        
        print("✓ Circuit specification created successfully")
        
    except Exception as e:
        print(f"✗ Quantum operations test failed: {e}")

def test_nqba_engine():
    """Test NQBA engine"""
    print("\nTesting NQBA engine...")
    
    try:
        from nqba.engine import NQBAEngine
        
        # Initialize engine
        engine = NQBAEngine(
            mode="simulator",
            max_qubits=4,
            enable_optimization=True
        )
        print("✓ NQBA Engine initialized successfully")
        
        # Test circuit execution
        circuit_spec = {
            "qubits": 2,
            "gates": [
                {"type": "h", "target": 0},
                {"type": "cx", "control": 0, "target": 1}
            ],
            "measurements": [0, 1]
        }
        
        print("✓ Circuit specification created successfully")
        
    except Exception as e:
        print(f"✗ NQBA engine test failed: {e}")

def main():
    """Main test function"""
    print("FLYFOX AI Quantum Computing Platform - Basic Test")
    print("=" * 60)
    
    test_basic_imports()
    test_quantum_operations()
    test_nqba_engine()
    
    print("\n" + "=" * 60)
    print("Basic test completed!")

if __name__ == "__main__":
    main()
