#!/usr/bin/env python3
"""
Simple integration test for Goliath Quantum
Tests basic functionality of the NQBA components
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nqba.engine import QuantumEngine, QuantumTask, ExecutionMode
from nqba.quantum_adapter import DynexQuantumAdapter
from nqba.decision_logic import DecisionEngine


async def test_basic_functionality():
    """Test basic functionality of all components"""
    print("🧪 Testing Goliath Quantum Integration...")
    
    try:
        # Test 1: Quantum Adapter
        print("\n1. Testing Quantum Adapter...")
        adapter = DynexQuantumAdapter()
        connected = await adapter.connect()
        assert connected, "Failed to connect quantum adapter"
        print("✅ Quantum Adapter: Connected successfully")
        
        # Test 2: Decision Engine
        print("\n2. Testing Decision Engine...")
        decision_engine = DecisionEngine()
        await decision_engine.initialize()
        status = await decision_engine.get_status()
        assert status["initialized"], "Failed to initialize decision engine"
        print("✅ Decision Engine: Initialized successfully")
        
        # Test 3: Quantum Engine
        print("\n3. Testing Quantum Engine...")
        engine = QuantumEngine()
        await engine.initialize()
        engine_status = await engine.get_engine_status()
        assert engine_status["running"], "Failed to start quantum engine"
        print("✅ Quantum Engine: Started successfully")
        
        # Test 4: Circuit Execution
        print("\n4. Testing Circuit Execution...")
        circuit = """
        OPENQASM 2.0;
        include "qelib1.inc";
        qreg q[2];
        creg c[2];
        h q[0];
        cx q[0], q[1];
        measure q[0] -> c[0];
        measure q[1] -> c[1];
        """
        
        task = QuantumTask(
            task_id="test_task_001",
            circuit=circuit,
            parameters={"shots": 1000},
            mode=ExecutionMode.SIMULATION,
            priority=1
        )
        
        result = await engine.execute_task(task)
        assert result["status"] == "completed", "Task execution failed"
        print("✅ Circuit Execution: Completed successfully")
        
        # Test 5: Decision Processing
        print("\n5. Testing Decision Processing...")
        quantum_result = result["quantum_result"]
        context = {
            "decision_type": "investment",
            "market_data": {"symbol": "AAPL", "price": 150.0},
            "risk_tolerance": 0.5
        }
        
        decision_result = await decision_engine.process_result(quantum_result, context)
        assert "recommendation" in decision_result, "Decision processing failed"
        print("✅ Decision Processing: Completed successfully")
        
        # Test 6: Cleanup
        print("\n6. Testing Cleanup...")
        await engine.shutdown()
        await decision_engine.shutdown()
        await adapter.disconnect()
        print("✅ Cleanup: Completed successfully")
        
        print("\n🎉 All tests passed! Goliath Quantum is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


async def test_agent_imports():
    """Test that agent modules can be imported"""
    print("\n🧪 Testing Agent Imports...")
    
    try:
        from agents.chatbot import QuantumChatbot
        from agents.voice_agent import QuantumVoiceAgent
        from agents.digital_human import QuantumDigitalHuman
        print("✅ Agent Imports: All agent modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False


async def test_utility_imports():
    """Test that utility modules can be imported"""
    print("\n🧪 Testing Utility Imports...")
    
    try:
        from utils.config import ConfigManager, get_config
        from utils.logger import get_logger, setup_logging
        print("✅ Utility Imports: All utility modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Utility import failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🚀 Starting Goliath Quantum Integration Tests")
    print("=" * 50)
    
    # Run all tests
    tests = [
        test_basic_functionality(),
        test_agent_imports(),
        test_utility_imports()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Check results
    passed = 0
    total = len(results)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Test {i+1} failed with exception: {result}")
        elif result:
            passed += 1
        else:
            print(f"❌ Test {i+1} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The repo-ready package is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
