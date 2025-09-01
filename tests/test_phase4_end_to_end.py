"""
NQBA Phase 4: End-to-End Testing

This module provides comprehensive end-to-end testing for the complete NQBA ecosystem,
including business unit integration, API functionality, and cross-unit communication.
"""

import pytest
import pytest_asyncio
import asyncio
import time
from typing import Dict, Any, List
from fastapi.testclient import TestClient

from nqba_stack.api.main import app
from nqba_stack.business_integration import (
    BusinessUnitManager,
    FLYFOXAIBusinessUnit,
    BusinessUnitType,
    BusinessUnitStatus,
)
from nqba_stack.quantum.adapters.dynex_adapter import DynexAdapter


class TestPhase4EndToEnd:
    """Test Phase 4 end-to-end ecosystem integration"""

    @pytest_asyncio.fixture
    async def business_unit_manager(self):
        """Create a business unit manager for testing"""
        manager = BusinessUnitManager()
        yield manager
        await manager.stop_monitoring()

    @pytest_asyncio.fixture
    async def flyfox_ai_unit(self):
        """Create a FLYFOX AI business unit for testing"""
        unit = FLYFOXAIBusinessUnit()
        yield unit
        await unit.shutdown()

    @pytest_asyncio.fixture
    async def dynex_adapter(self):
        """Create a Dynex adapter for testing"""
        adapter = DynexAdapter()
        yield adapter

    @pytest.fixture
    def api_client(self):
        """Create a FastAPI test client"""
        return TestClient(app)

    @pytest_asyncio.fixture
    async def initialized_ecosystem(self, business_unit_manager, flyfox_ai_unit):
        """Initialize the complete NQBA ecosystem for testing"""
        # Register FLYFOX AI business unit
        await business_unit_manager.register_business_unit(flyfox_ai_unit)

        # Start monitoring
        await business_unit_manager.start_monitoring()

        # Wait for initialization
        await asyncio.sleep(0.1)

        yield business_unit_manager

        # Cleanup
        await business_unit_manager.stop_monitoring()

    # ============================================================================
    # ECOSYSTEM INTEGRATION TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_ecosystem_initialization(self, initialized_ecosystem):
        """Test complete ecosystem initialization and startup"""
        # Verify business unit manager is running
        assert initialized_ecosystem.is_monitoring

        # Verify FLYFOX AI is registered and active
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        assert len(flyfox_units) == 1

        flyfox_unit = flyfox_units[0]
        assert flyfox_unit.status == BusinessUnitStatus.ACTIVE
        assert flyfox_unit.is_initialized

        # Verify monitoring is active
        metrics = await initialized_ecosystem.get_ecosystem_metrics()
        assert metrics["total_business_units"] == 1
        assert metrics["active_business_units"] == 1
        assert metrics["ecosystem_health"] == "healthy"

    @pytest.mark.asyncio
    async def test_cross_unit_communication(self, initialized_ecosystem):
        """Test communication between different business units"""
        # Get all business units
        all_units = await initialized_ecosystem.get_all_business_units()
        assert len(all_units) == 1

        # Test cross-unit operation execution
        flyfox_unit = all_units[0]

        # Execute a complex operation that involves multiple components
        result = await flyfox_unit.execute_operation(
            "comprehensive_energy_analysis",
            {
                "consumption_data": {
                    "peak_hours": [14, 15, 16],
                    "usage": [100, 120, 110],
                },
                "optimization_targets": ["cost", "efficiency", "carbon_footprint"],
                "quantum_optimization": True,
            },
        )

        assert result["success"] is True
        assert "quantum_advantage" in result
        assert "optimization_results" in result
        assert "cross_unit_insights" in result

    # ============================================================================
    # API INTEGRATION TESTS
    # ============================================================================

    def test_api_ecosystem_status(self, api_client):
        """Test the ecosystem status endpoint through the API"""
        response = api_client.get("/api/v1/ecosystem/status")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "ecosystem_health" in data["data"]
        assert "business_units" in data["data"]
        assert "quantum_advantage" in data["data"]

    def test_api_flyfox_ai_operations(self, api_client):
        """Test FLYFOX AI operations through the API"""
        # Test energy optimization
        optimization_request = {
            "consumption_data": {"peak_hours": [14, 15, 16], "usage": [100, 120, 110]},
            "optimization_targets": ["cost", "efficiency"],
            "quantum_optimization": True,
        }

        response = api_client.post(
            "/api/v1/flyfox-ai/optimize-energy", json=optimization_request
        )
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "quantum_advantage" in data
        assert data["data"]["optimization_results"]["cost_savings"] > 0

        # Test consumption analysis
        analysis_request = {
            "time_period": "24h",
            "analysis_type": "pattern_recognition",
        }

        response = api_client.post(
            "/api/v1/flyfox-ai/analyze-consumption", json=analysis_request
        )
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "consumption_patterns" in data["data"]

    def test_api_error_handling(self, api_client):
        """Test API error handling and validation"""
        # Test invalid request data
        invalid_request = {"invalid_field": "invalid_value"}

        response = api_client.post(
            "/api/v1/flyfox-ai/optimize-energy", json=invalid_request
        )
        assert response.status_code == 422  # Validation error

        # Test non-existent endpoint
        response = api_client.get("/api/v1/non-existent")
        assert response.status_code == 404

    # ============================================================================
    # QUANTUM INTEGRATION TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_quantum_optimization_integration(
        self, dynex_adapter, flyfox_ai_unit
    ):
        """Test quantum optimization integration with business units"""
        # Create a QUBO problem for energy optimization
        qubo_data = {
            "description": "FLYFOX AI Energy Optimization QUBO",
            "variables": ["solar", "wind", "battery", "grid"],
            "constraints": {
                "total_power": 1000,
                "max_cost": 500,
                "min_efficiency": 0.85,
            },
            "objective": "minimize_cost_maximize_efficiency",
        }

        # Submit QUBO to quantum solver
        job_id = await dynex_adapter.submit_qubo(qubo_data)
        assert job_id is not None
        assert job_id.startswith("dynex_")

        # Wait for job completion
        await asyncio.sleep(0.1)

        # Check job status
        job_status = await dynex_adapter.get_job_status(job_id)
        assert job_status["status"] in ["completed", "running", "pending"]

        # Get results
        results = await dynex_adapter.get_job_results(job_id)
        assert "samples" in results
        assert "energy" in results

    @pytest.mark.asyncio
    async def test_quantum_advantage_calculation(self, flyfox_ai_unit):
        """Test quantum advantage calculation in business operations"""
        # Execute energy optimization with quantum enhancement
        result = await flyfox_unit.execute_operation(
            "quantum_enhanced_optimization",
            {
                "optimization_type": "energy_mix",
                "quantum_enhancement": True,
                "classical_baseline": True,
            },
        )

        assert result["success"] is True
        assert "quantum_advantage" in result
        assert "classical_performance" in result
        assert "quantum_performance" in result

        # Verify quantum advantage calculation
        quantum_advantage = result["quantum_advantage"]
        assert quantum_advantage > 1.0  # Should show improvement
        assert quantum_advantage <= 10.0  # Realistic upper bound

    # ============================================================================
    # PERFORMANCE AND LOAD TESTING
    # ============================================================================

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, initialized_ecosystem):
        """Test concurrent operation execution"""
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        # Execute multiple operations concurrently
        start_time = time.time()

        tasks = []
        for i in range(5):
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
            assert result["success"] is True

        # Verify performance (should complete within reasonable time)
        execution_time = end_time - start_time
        assert execution_time < 5.0  # Should complete within 5 seconds

    def test_api_response_time(self, api_client):
        """Test API response time performance"""
        # Test multiple endpoints for response time
        endpoints = ["/", "/health", "/api/v1/ecosystem/status", "/api/v1/flyfox-ai"]

        for endpoint in endpoints:
            start_time = time.time()
            response = api_client.get(endpoint)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            assert response_time < 100  # Should respond within 100ms
            assert response.status_code == 200

    # ============================================================================
    # ERROR RECOVERY AND RESILIENCE TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_business_unit_recovery(self, initialized_ecosystem):
        """Test business unit recovery after failures"""
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        # Simulate a failure scenario
        try:
            await flyfox_unit.execute_operation(
                "invalid_operation", {"invalid_data": "should_fail"}
            )
        except Exception:
            pass  # Expected to fail

        # Verify the unit is still operational
        assert flyfox_unit.status == BusinessUnitStatus.ACTIVE
        assert flyfox_unit.is_initialized

        # Verify it can still execute valid operations
        result = await flyfox_unit.execute_operation(
            "energy_consumption_analysis", {"time_period": "1h"}
        )
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_ecosystem_health_monitoring(self, initialized_ecosystem):
        """Test ecosystem health monitoring and alerting"""
        # Get initial health status
        initial_health = await initialized_ecosystem.get_ecosystem_health()
        assert initial_health["status"] == "healthy"

        # Simulate a business unit issue
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        # Temporarily change status to simulate issue
        original_status = flyfox_unit.status
        flyfox_unit.status = BusinessUnitStatus.ERROR

        # Check health monitoring detects the issue
        health_check = await initialized_ecosystem.get_ecosystem_health()
        assert health_check["status"] == "degraded"
        assert "issues" in health_check

        # Restore normal status
        flyfox_unit.status = original_status

        # Verify health returns to normal
        final_health = await initialized_ecosystem.get_ecosystem_health()
        assert final_health["status"] == "healthy"

    # ============================================================================
    # DATA FLOW AND INTEGRATION TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_data_flow_through_ecosystem(self, initialized_ecosystem):
        """Test data flow through the complete ecosystem"""
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        # Execute a data-intensive operation
        result = await flyfox_unit.execute_operation(
            "comprehensive_energy_analysis",
            {
                "consumption_data": {
                    "hourly_data": [100 + i * 0.1 for i in range(24)],
                    "weather_data": {"temperature": [20 + i * 0.5 for i in range(24)]},
                    "pricing_data": {
                        "electricity_rate": [0.12 + i * 0.01 for i in range(24)]
                    },
                },
                "analysis_parameters": {
                    "time_resolution": "1h",
                    "optimization_horizon": "24h",
                    "include_weather_correlation": True,
                },
            },
        )

        assert result["success"] is True

        # Verify data processing results
        data = result["data"]
        assert "consumption_analysis" in data
        assert "weather_correlation" in data
        assert "pricing_optimization" in data
        assert "recommendations" in data

        # Verify quantum advantage calculation
        assert "quantum_advantage" in result
        assert result["quantum_advantage"] > 1.0

    @pytest.mark.asyncio
    async def test_metrics_tracking_and_reporting(self, initialized_ecosystem):
        """Test metrics tracking and reporting across the ecosystem"""
        # Get ecosystem metrics
        metrics = await initialized_ecosystem.get_ecosystem_metrics()

        # Verify metrics structure
        assert "total_business_units" in metrics
        assert "active_business_units" in metrics
        assert "ecosystem_health" in metrics
        assert "performance_metrics" in metrics

        # Execute operations to generate metrics
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        await flyfox_unit.execute_operation(
            "energy_consumption_analysis", {"time_period": "1h"}
        )

        # Get updated metrics
        updated_metrics = await initialized_ecosystem.get_ecosystem_metrics()

        # Verify metrics have been updated
        assert updated_metrics["performance_metrics"]["total_operations"] > 0
        assert updated_metrics["performance_metrics"]["successful_operations"] > 0

    # ============================================================================
    # INTEGRATION VALIDATION TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_complete_workflow_integration(
        self, initialized_ecosystem, dynex_adapter
    ):
        """Test complete workflow integration from data input to quantum optimization"""
        flyfox_units = await initialized_ecosystem.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        flyfox_unit = flyfox_units[0]

        # Step 1: Data collection and analysis
        analysis_result = await flyfox_unit.execute_operation(
            "energy_consumption_analysis",
            {
                "time_period": "24h",
                "data_sources": ["smart_meters", "weather_api", "pricing_api"],
                "analysis_depth": "comprehensive",
            },
        )

        assert analysis_result["success"] is True
        analysis_data = analysis_result["data"]

        # Step 2: Pattern recognition and forecasting
        forecast_result = await flyfox_unit.execute_operation(
            "demand_forecasting",
            {
                "historical_data": analysis_data["consumption_patterns"],
                "forecast_horizon": "7d",
                "confidence_level": 0.95,
            },
        )

        assert forecast_result["success"] is True
        forecast_data = forecast_result["data"]

        # Step 3: Quantum optimization
        optimization_result = await flyfox_unit.execute_operation(
            "quantum_enhanced_optimization",
            {
                "forecast_data": forecast_data,
                "optimization_targets": ["cost", "efficiency", "carbon_footprint"],
                "constraints": {
                    "max_budget": 1000,
                    "min_efficiency": 0.9,
                    "carbon_target": 0.5,
                },
            },
        )

        assert optimization_result["success"] is True

        # Step 4: Verify quantum advantage
        assert "quantum_advantage" in optimization_result
        quantum_advantage = optimization_result["quantum_advantage"]
        assert quantum_advantage > 1.0

        # Step 5: Verify complete workflow results
        final_data = optimization_result["data"]
        assert "optimization_results" in final_data
        assert "cost_savings" in final_data["optimization_results"]
        assert "efficiency_improvement" in final_data["optimization_results"]
        assert "carbon_reduction" in final_data["optimization_results"]

    def test_api_documentation_accessibility(self, api_client):
        """Test API documentation accessibility and completeness"""
        # Test OpenAPI documentation
        response = api_client.get("/docs")
        assert response.status_code == 200

        # Test ReDoc documentation
        response = api_client.get("/redoc")
        assert response.status_code == 200

        # Test OpenAPI schema
        response = api_client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "paths" in schema
        assert "components" in schema

        # Verify FLYFOX AI endpoints are documented
        flyfox_paths = [path for path in schema["paths"].keys() if "flyfox-ai" in path]
        assert len(flyfox_paths) > 0

        # Verify business unit endpoints are documented
        business_paths = [path for path in schema["paths"].keys() if "business" in path]
        assert len(business_paths) > 0
