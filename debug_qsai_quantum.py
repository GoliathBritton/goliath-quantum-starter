#!/usr/bin/env python3
"""
Debug script to test QSAICore quantum integration
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Testing QSAICore quantum integration...")

try:
    # Test import
    print("1. Testing QSAICore import...")
    from core.qsaiCore import QSAICore, QUANTUM_AVAILABLE
    print(f"   ✅ QSAICore imported successfully")
    print(f"   QUANTUM_AVAILABLE flag: {QUANTUM_AVAILABLE}")
    
    # Test initialization
    print("2. Testing QSAICore initialization...")
    core = QSAICore()
    print("   ✅ QSAICore initialized successfully")
    
    # Test quantum hub availability
    print("3. Testing quantum hub availability...")
    print(f"   quantum_hub attribute exists: {hasattr(core, 'quantum_hub')}")
    print(f"   quantum_hub value: {core.quantum_hub}")
    print(f"   quantum_hub is not None: {core.quantum_hub is not None}")
    
    if core.quantum_hub:
        print(f"   Available solvers: {list(core.quantum_hub.solvers.keys())}")
        print("   🎉 Quantum hub is available and working!")
    else:
        print("   ⚠️  Quantum hub is None - initialization failed")
    
except ImportError as e:
    print(f"   ❌ Import error: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()