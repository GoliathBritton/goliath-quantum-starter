#!/usr/bin/env python3
"""
Debug script to test QuantumIntegrationHub initialization
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Testing QuantumIntegrationHub initialization...")

try:
    # Test import
    print("1. Testing imports...")
    from src.nqba_stack.quantum.qih import QuantumIntegrationHub
    print("   ✅ QuantumIntegrationHub imported successfully")
    
    # Test initialization
    print("2. Testing initialization...")
    hub = QuantumIntegrationHub()
    print("   ✅ QuantumIntegrationHub initialized successfully")
    
    # Test basic functionality
    print("3. Testing basic functionality...")
    print(f"   Available solvers: {list(hub.solvers.keys())}")
    print(f"   Circuit breaker state: {hub.circuit_breaker.state}")
    
    print("\n🎉 All tests passed! QuantumIntegrationHub is working correctly.")
    
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    print("   This suggests missing dependencies or import path issues.")
except Exception as e:
    print(f"   ❌ Initialization error: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()