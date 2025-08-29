#!/usr/bin/env python3
"""
Simple Phase 4 Test Script
Tests the NQBA ecosystem integration without pytest
"""

import asyncio
import time
from nqba_stack.business_integration import (
    BusinessUnitManager,
    FLYFOXAIBusinessUnit,
    BusinessUnitType,
    BusinessUnitStatus,
)
from nqba_stack.api.main import app
from fastapi.testclient import TestClient


async def test_ecosystem_initialization():
    """Test complete ecosystem initialization and startup"""
    print("🔧 Testing ecosystem initialization...")

    # Create business unit manager
    manager = BusinessUnitManager()

    # Create FLYFOX AI business unit
    flyfox_unit = FLYFOXAIBusinessUnit()

    # Register business unit
    await manager.register_business_unit(flyfox_unit)

    # Start monitoring
    await manager.start_monitoring()

    # Wait for initialization
    await asyncio.sleep(0.1)

    # Verify business unit manager is running
    assert manager.is_monitoring, "Manager should be monitoring"
    print("✅ Business unit manager is monitoring")

    # Verify FLYFOX AI is registered and active
    flyfox_units = await manager.get_business_units_by_type(BusinessUnitType.FLYFOX_AI)
    assert len(flyfox_units) == 1, "Should have 1 FLYFOX AI unit"

    flyfox_unit = flyfox_units[0]
    assert flyfox_unit.status == BusinessUnitStatus.ACTIVE, "Unit should be active"
    assert flyfox_unit.is_initialized, "Unit should be initialized"
    print("✅ FLYFOX AI business unit is active and initialized")

    # Verify monitoring is active
    metrics = await manager.get_ecosystem_metrics()
    assert metrics["total_business_units"] == 1, "Should have 1 total unit"
    assert metrics["active_business_units"] == 1, "Should have 1 active unit"
    assert metrics["ecosystem_health"] == "healthy", "Ecosystem should be healthy"
    print("✅ Ecosystem metrics are correct")

    # Cleanup
    await manager.stop_monitoring()
    await flyfox_unit.shutdown()

    print("✅ Ecosystem initialization test passed!")


async def test_business_unit_operations():
    """Test business unit operations"""
    print("🔧 Testing business unit operations...")

    # Create and initialize business unit
    flyfox_unit = FLYFOXAIBusinessUnit()

    # Test energy consumption analysis
    result = await flyfox_unit.execute_operation(
        "energy_consumption_analysis", {"time_period": "1h"}
    )

    assert result["success"] is True, "Operation should succeed"
    assert "quantum_advantage" in result, "Should have quantum advantage"
    print("✅ Energy consumption analysis works")

    # Test energy optimization
    result = await flyfox_unit.execute_operation(
        "optimize_energy_consumption",
        {
            "consumption_data": {"peak_hours": [14, 15, 16], "usage": [100, 120, 110]},
            "optimization_targets": ["cost", "efficiency"],
        },
    )

    assert result["success"] is True, "Optimization should succeed"
    assert "optimization_results" in result["data"], "Should have optimization results"
    print("✅ Energy optimization works")

    # Cleanup
    await flyfox_unit.shutdown()

    print("✅ Business unit operations test passed!")


def test_api_endpoints():
    """Test API endpoints"""
    print("🔧 Testing API endpoints...")

    # Create test client
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200, "Root endpoint should return 200"
    data = response.json()
    assert (
        data["message"]
        == "Welcome to NQBA (Neuromorphic Quantum Business Architecture) API"
    )
    print("✅ Root endpoint works")

    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200, "Health endpoint should return 200"
    print("✅ Health endpoint works")

    # Test ecosystem status endpoint
    response = client.get("/api/v1/ecosystem/status")
    assert response.status_code == 200, "Ecosystem status should return 200"
    data = response.json()
    assert data["success"] is True, "Ecosystem status should be successful"
    print("✅ Ecosystem status endpoint works")

    # Test FLYFOX AI endpoint
    response = client.get("/api/v1/flyfox-ai")
    assert response.status_code == 200, "FLYFOX AI endpoint should return 200"
    data = response.json()
    assert data["success"] is True, "FLYFOX AI endpoint should be successful"
    print("✅ FLYFOX AI endpoint works")

    print("✅ API endpoints test passed!")


async def test_quantum_integration():
    """Test quantum integration"""
    print("🔧 Testing quantum integration...")

    from nqba_stack.quantum.adapters.dynex_adapter import DynexAdapter

    # Create Dynex adapter
    adapter = DynexAdapter()

    # Create a QUBO problem for energy optimization
    qubo_data = {
        "description": "FLYFOX AI Energy Optimization QUBO",
        "variables": ["solar", "wind", "battery", "grid"],
        "constraints": {"total_power": 1000, "max_cost": 500, "min_efficiency": 0.85},
        "objective": "minimize_cost_maximize_efficiency",
    }

    # Submit QUBO to quantum solver
    job_id = await adapter.submit_qubo(qubo_data)
    assert job_id is not None, "Job ID should not be None"
    assert job_id.startswith("dynex_"), "Job ID should start with 'dynex_'"
    print("✅ QUBO submission works")

    # Wait for job completion
    await asyncio.sleep(0.1)

    # Check job status
    job_status = await adapter.get_job_status(job_id)
    assert job_status["status"] in [
        "completed",
        "running",
        "pending",
    ], "Job should have valid status"
    print("✅ Job status check works")

    # Get results
    results = await adapter.get_job_results(job_id)
    assert "samples" in results, "Results should have samples"
    assert "energy" in results, "Results should have energy"
    print("✅ Job results retrieval works")

    print("✅ Quantum integration test passed!")


async def test_performance():
    """Test performance metrics"""
    print("🔧 Testing performance...")

    # Create business unit
    flyfox_unit = FLYFOXAIBusinessUnit()

    # Test concurrent operations
    start_time = time.time()

    tasks = []
    for i in range(3):
        task = flyfox_unit.execute_operation(
            "energy_consumption_analysis",
            {"analysis_id": f"test_{i}", "time_period": "1h"},
        )
        tasks.append(task)

    # Wait for all operations to complete
    results = await asyncio.gather(*tasks)
    end_time = time.time()

    # Verify all operations completed successfully
    for result in results:
        assert result["success"] is True, "All operations should succeed"

    # Verify performance (should complete within reasonable time)
    execution_time = end_time - start_time
    assert (
        execution_time < 3.0
    ), f"Should complete within 3 seconds, took {execution_time:.2f}s"
    print(f"✅ Concurrent operations completed in {execution_time:.2f}s")

    # Cleanup
    await flyfox_unit.shutdown()

    print("✅ Performance test passed!")


async def main():
    """Run all Phase 4 tests"""
    print("🚀 Starting NQBA Phase 4 End-to-End Testing")
    print("=" * 60)

    try:
        # Test ecosystem initialization
        await test_ecosystem_initialization()
        print()

        # Test business unit operations
        await test_business_unit_operations()
        print()

        # Test API endpoints
        test_api_endpoints()
        print()

        # Test quantum integration
        await test_quantum_integration()
        print()

        # Test performance
        await test_performance()
        print()

        print("=" * 60)
        print("🎉 ALL PHASE 4 TESTS PASSED!")
        print("✅ NQBA Ecosystem is fully operational")
        print("✅ Business Unit Integration is working")
        print("✅ API Endpoints are functional")
        print("✅ Quantum Integration is operational")
        print("✅ Performance meets requirements")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    exit(0 if success else 1)
