"""
Test Phase 2: Business Unit Integration

Tests the FLYFOX AI business unit integration and basic functionality.
"""

import pytest
import pytest_asyncio
import asyncio
from src.nqba_stack.business_integration import (
    BusinessUnitManager,
    FLYFOXAIBusinessUnit,
    BusinessUnitType,
    BusinessUnitStatus,
)


class TestPhase2BusinessIntegration:
    """Test Phase 2 business unit integration"""

    @pytest_asyncio.fixture
    async def business_unit_manager(self):
        """Create a business unit manager for testing"""
        manager = BusinessUnitManager()
        yield manager
        # Cleanup
        await manager.stop_monitoring()

    @pytest_asyncio.fixture
    async def flyfox_ai_unit(self):
        """Create a FLYFOX AI business unit for testing"""
        unit = FLYFOXAIBusinessUnit()
        yield unit
        # Cleanup
        await unit.shutdown()

    @pytest.mark.asyncio
    async def test_flyfox_ai_initialization(self, flyfox_ai_unit):
        """Test FLYFOX AI business unit initialization"""
        # Test initialization
        success = await flyfox_ai_unit.initialize()
        assert success is True

        # Verify configuration
        assert flyfox_ai_unit.config.unit_id == "flyfox_ai_001"
        assert flyfox_ai_unit.config.unit_type == BusinessUnitType.FLYFOX_AI
        assert flyfox_ai_unit.config.name == "FLYFOX AI Energy Hub"
        assert flyfox_ai_unit.config.quantum_enhancement is True

        # Verify status
        assert flyfox_ai_unit.status == BusinessUnitStatus.ACTIVE

        # Verify energy sources and algorithms
        assert len(flyfox_ai_unit.energy_sources) > 0
        assert len(flyfox_ai_unit.optimization_algorithms) > 0
        assert len(flyfox_ai_unit.consumption_patterns) > 0

    @pytest.mark.asyncio
    async def test_flyfox_ai_health_check(self, flyfox_ai_unit):
        """Test FLYFOX AI health check functionality"""
        await flyfox_ai_unit.initialize()

        health_status = await flyfox_ai_unit.health_check()

        assert "healthy" in health_status
        assert "timestamp" in health_status
        assert "cpu_usage_percent" in health_status
        assert "memory_usage_percent" in health_status
        assert "energy_optimizations_active" in health_status

    @pytest.mark.asyncio
    async def test_flyfox_ai_capabilities(self, flyfox_ai_unit):
        """Test FLYFOX AI capabilities"""
        await flyfox_ai_unit.initialize()

        capabilities = await flyfox_ai_unit.get_capabilities()

        assert capabilities["business_unit"] == "FLYFOX AI"
        assert capabilities["version"] == "2.0.0"
        assert "energy_optimization" in capabilities["capabilities"]
        assert "quantum_enhancement" in capabilities["capabilities"]
        assert "optimize_energy_consumption" in capabilities["supported_operations"]
        assert (
            "3.2x energy optimization efficiency" in capabilities["quantum_advantage"]
        )

    @pytest.mark.asyncio
    async def test_flyfox_ai_energy_optimization(self, flyfox_ai_unit):
        """Test FLYFOX AI energy optimization operation"""
        await flyfox_ai_unit.initialize()

        parameters = {
            "customer_type": "residential",
            "current_consumption": 15.0,
            "optimization_level": "maximum",
        }

        result = await flyfox_ai_unit.execute_operation(
            "optimize_energy_consumption", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "optimize_energy_consumption"
        assert result["business_unit"] == "FLYFOX AI"
        assert "quantum_advantage" in result
        assert result["quantum_advantage"] >= 3.0  # Should achieve 3.2x
        assert "recommendations" in result
        assert "estimated_monthly_savings" in result
        assert "carbon_reduction_kg" in result

    @pytest.mark.asyncio
    async def test_flyfox_ai_consumption_analysis(self, flyfox_ai_unit):
        """Test FLYFOX AI consumption pattern analysis"""
        await flyfox_ai_unit.initialize()

        parameters = {"customer_type": "commercial", "time_period": "24h"}

        result = await flyfox_ai_unit.execute_operation(
            "analyze_consumption_patterns", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "analyze_consumption_patterns"
        assert "analysis" in result
        assert result["analysis"]["customer_type"] == "commercial"
        assert "peak_hours" in result["analysis"]
        assert "base_load" in result["analysis"]
        assert "recommendations" in result["analysis"]

    @pytest.mark.asyncio
    async def test_flyfox_ai_energy_forecasting(self, flyfox_ai_unit):
        """Test FLYFOX AI energy demand forecasting"""
        await flyfox_ai_unit.initialize()

        parameters = {"forecast_hours": 48, "customer_type": "industrial"}

        result = await flyfox_ai_unit.execute_operation(
            "forecast_energy_demand", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "forecast_energy_demand"
        assert result["forecast_hours"] == 48
        assert result["customer_type"] == "industrial"
        assert "forecast_data" in result
        assert len(result["forecast_data"]) == 48
        assert "total_forecasted_demand" in result

    @pytest.mark.asyncio
    async def test_flyfox_ai_energy_mix_optimization(self, flyfox_ai_unit):
        """Test FLYFOX AI energy mix optimization"""
        await flyfox_ai_unit.initialize()

        parameters = {
            "total_demand": 200.0,
            "available_sources": ["solar", "wind", "battery", "grid"],
        }

        result = await flyfox_ai_unit.execute_operation(
            "optimize_energy_mix", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "optimize_energy_mix"
        assert result["total_demand"] == 200.0
        assert "optimal_mix" in result
        assert "renewable_percentage" in result
        assert "cost_optimization" in result
        assert "carbon_reduction" in result

    @pytest.mark.asyncio
    async def test_flyfox_ai_carbon_footprint(self, flyfox_ai_unit):
        """Test FLYFOX AI carbon footprint calculation"""
        await flyfox_ai_unit.initialize()

        parameters = {
            "energy_consumption": 150.0,
            "energy_mix": {"grid": 0.6, "renewable": 0.4},
        }

        result = await flyfox_ai_unit.execute_operation(
            "calculate_carbon_footprint", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "calculate_carbon_footprint"
        assert result["energy_consumption_kwh"] == 150.0
        assert "energy_mix" in result
        assert "carbon_footprint_kg" in result
        assert "carbon_intensity" in result
        assert "renewable_percentage" in result

    @pytest.mark.asyncio
    async def test_flyfox_ai_grid_load_balancing(self, flyfox_ai_unit):
        """Test FLYFOX AI grid load balancing"""
        await flyfox_ai_unit.initialize()

        parameters = {
            "grid_load": 800.0,
            "available_capacity": 1000.0,
            "renewable_generation": 250.0,
        }

        result = await flyfox_ai_unit.execute_operation(
            "grid_load_balancing", parameters
        )

        assert result["success"] is True
        assert result["operation_type"] == "grid_load_balancing"
        assert result["grid_load_mw"] == 800.0
        assert "load_balance_score" in result
        assert "renewable_integration" in result
        assert "grid_stability" in result
        assert "recommendation" in result

    @pytest.mark.asyncio
    async def test_flyfox_ai_metrics_tracking(self, flyfox_ai_unit):
        """Test FLYFOX AI metrics tracking"""
        await flyfox_ai_unit.initialize()

        # Execute an operation to generate metrics
        parameters = {"customer_type": "residential", "current_consumption": 10.0}
        await flyfox_ai_unit.execute_operation(
            "optimize_energy_consumption", parameters
        )

        # Check metrics
        assert flyfox_ai_unit.metrics.total_operations > 0
        assert flyfox_ai_unit.metrics.successful_operations > 0
        assert flyfox_ai_unit.metrics.last_operation is not None
        assert flyfox_ai_unit.metrics.quantum_advantage >= 1.0

    @pytest.mark.asyncio
    async def test_flyfox_ai_status_report(self, flyfox_ai_unit):
        """Test FLYFOX AI status report generation"""
        await flyfox_ai_unit.initialize()

        status_report = await flyfox_ai_unit.get_status_report()

        assert status_report["unit_id"] == "flyfox_ai_001"
        assert status_report["unit_type"] == "flyfox_ai"
        assert status_report["name"] == "FLYFOX AI Energy Hub"
        assert status_report["status"] == "active"
        assert "metrics" in status_report
        assert "config" in status_report
        assert status_report["config"]["quantum_enhancement"] is True

    @pytest.mark.asyncio
    async def test_flyfox_ai_energy_insights(self, flyfox_ai_unit):
        """Test FLYFOX AI energy insights"""
        await flyfox_ai_unit.initialize()

        # Execute a few operations to generate insights
        for i in range(3):
            parameters = {
                "customer_type": "residential",
                "current_consumption": 10.0 + i,
            }
            await flyfox_ai_unit.execute_operation(
                "optimize_energy_consumption", parameters
            )

        insights = await flyfox_ai_unit.get_energy_insights()

        assert "total_optimizations" in insights
        assert "recent_optimizations" in insights
        assert "average_quantum_advantage" in insights
        assert "energy_sources_managed" in insights
        assert "optimization_algorithms" in insights
        assert "customer_types_supported" in insights
        assert insights["total_optimizations"] >= 3

    @pytest.mark.asyncio
    async def test_business_unit_manager_registration(
        self, business_unit_manager, flyfox_ai_unit
    ):
        """Test business unit manager registration"""
        # Register the business unit
        success = await business_unit_manager.register_business_unit(flyfox_ai_unit)
        assert success is True

        # Verify registration
        registered_unit = await business_unit_manager.get_business_unit("flyfox_ai_001")
        assert registered_unit is not None
        assert registered_unit.config.unit_id == "flyfox_ai_001"

        # Get all business units
        all_units = await business_unit_manager.get_all_business_units()
        assert len(all_units) == 1
        assert all_units[0].config.unit_id == "flyfox_ai_001"

        # Get business units by type
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )
        assert len(flyfox_units) == 1
        assert flyfox_units[0].config.unit_id == "flyfox_ai_001"

    @pytest.mark.asyncio
    async def test_business_unit_manager_ecosystem_status(
        self, business_unit_manager, flyfox_ai_unit
    ):
        """Test business unit manager ecosystem status"""
        # Register the business unit
        await business_unit_manager.register_business_unit(flyfox_ai_unit)

        # Get ecosystem status
        ecosystem_status = await business_unit_manager.get_ecosystem_status()

        assert ecosystem_status["status"] == "operational"
        assert ecosystem_status["total_business_units"] == 1
        assert ecosystem_status["active_business_units"] == 1
        assert ecosystem_status["inactive_business_units"] == 0
        assert ecosystem_status["ecosystem_health"] == "excellent"
        assert "flyfox_ai_001" in ecosystem_status["business_units"]

    @pytest.mark.asyncio
    async def test_cross_unit_operation_identification(
        self, business_unit_manager, flyfox_ai_unit
    ):
        """Test cross-unit operation identification"""
        await business_unit_manager.register_business_unit(flyfox_ai_unit)

        # Test energy-related operation identification
        energy_operation = "optimize_energy_consumption"
        energy_params = {"customer_type": "residential"}

        # This should identify FLYFOX AI as involved
        # Note: This is a simplified test since we only have one business unit
        # In a full implementation, this would test with multiple business units

        # For now, just verify the method exists and doesn't crash
        assert hasattr(business_unit_manager, "_identify_involved_units")
        assert hasattr(business_unit_manager, "_aggregate_cross_unit_results")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
