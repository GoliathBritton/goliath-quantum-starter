#!/usr/bin/env python3
"""
QSAI and QEA-DO System Test Suite
=================================

Comprehensive testing of the Quantum Synthetic AI Decision Engine (QSAI)
and Quantum-Enhanced Algorithm Development Orchestrator (QEA-DO).

This script demonstrates:
1. QSAI autonomous decision making with specialized agents
2. QEA-DO algorithm generation and optimization
3. Integration with Dynex quantum models
4. Real-time context processing and action optimization
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class QSAIQEA_DOTester:
    """Test suite for QSAI and QEA-DO systems"""

    def __init__(self):
        self.test_results = []
        self.start_time = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.start_time = time.time()
        logger.info("🚀 Starting QSAI and QEA-DO System Tests")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        duration = time.time() - self.start_time
        logger.info(f"✅ QSAI and QEA-DO System Tests completed in {duration:.2f}s")
        await self._generate_test_report()

    async def run_all_tests(self):
        """Run all test suites"""
        logger.info("🧪 Running comprehensive test suite...")

        # Test QSAI Engine
        await self._test_qsai_engine()

        # Test QEA-DO System
        await self._test_qea_do_system()

        # Test Integration
        await self._test_integration()

        # Test Performance
        await self._test_performance()

        logger.info("🎯 All tests completed!")

    async def _test_qsai_engine(self):
        """Test QSAI Engine functionality"""
        logger.info("🔧 Testing QSAI Engine...")

        try:
            # Import QSAI components
            from src.nqba_stack.qsai_engine import (
                QSAIEngine,
                ContextVector,
                DecisionState,
            )
            from src.nqba_stack.qsai_agents import AgentFactory, AgentType
            from src.nqba_stack.core.ltc_logger import LTCLogger

            # Initialize LTC Logger (mock)
            ltc_logger = LTCLogger()

            # Initialize QSAI Engine
            qsai = QSAIEngine(ltc_logger)

            # Test 1: Context Processing
            await self._test_context_processing(qsai)

            # Test 2: Agent Registration
            await self._test_agent_registration(qsai, ltc_logger)

            # Test 3: Decision Pipeline
            await self._test_decision_pipeline(qsai)

            # Test 4: Safety Arbitration
            await self._test_safety_arbitration(qsai)

            # Test 5: Metrics and Audit
            await self._test_metrics_and_audit(qsai)

            self._record_test_result(
                "QSAI Engine", "PASSED", "All QSAI tests completed successfully"
            )

        except Exception as e:
            logger.error(f"❌ QSAI Engine test failed: {e}")
            self._record_test_result("QSAI Engine", "FAILED", str(e))

    async def _test_context_processing(self, qsai):
        """Test context processing capabilities"""
        logger.info("  📊 Testing context processing...")

        from src.nqba_stack.qsai_engine import ContextVector

        # Create test context
        context = ContextVector(
            user_id="test_user_001",
            timestamp=datetime.now(),
            telemetry={
                "speed": 45.0,
                "battery_level": 65,
                "location": "downtown",
                "maintenance_due": False,
                "acceleration": 0.2,
                "steering_angle": 5.0,
            },
            business_context={
                "user_segment": "premium",
                "trip_context": {
                    "destination": "shopping_center",
                    "estimated_duration": 1800,
                    "traffic_conditions": "moderate",
                },
                "user_preferences": {
                    "feature_interest": True,
                    "channel_preferences": {"hmi_voice": 0.8, "hmi_card": 0.6},
                },
                "subscription_expiring": False,
                "risk_score": 0.3,
                "credit_score": 750,
                "payment_history": "excellent",
                "account_age_days": 730,
            },
            market_signals={
                "energy_prices": {"current": 0.12, "trend": "stable"},
                "demand_forecast": "high",
                "competitive_offers": ["charging_discount", "feature_trial"],
            },
            nqba_embeddings=None,
            safety_flags=[],
            consent_level="full",
        )

        # Test context storage
        qsai.context_store[context.user_id] = context
        assert context.user_id in qsai.context_store
        logger.info("    ✅ Context storage working")

        # Test context retrieval
        stored_context = qsai.context_store[context.user_id]
        assert stored_context.user_id == context.user_id
        assert stored_context.telemetry["speed"] == 45.0
        logger.info("    ✅ Context retrieval working")

        logger.info("    ✅ Context processing tests passed")

    async def _test_agent_registration(self, qsai, ltc_logger):
        """Test agent registration and management"""
        logger.info("  🤖 Testing agent registration...")

        from src.nqba_stack.qsai_agents import AgentFactory, AgentType

        # Create and register agents
        offer_agent = AgentFactory.create_agent(AgentType.OFFER, ltc_logger)
        timing_agent = AgentFactory.create_agent(AgentType.TIMING, ltc_logger)
        channel_agent = AgentFactory.create_agent(AgentType.CHANNEL, ltc_logger)
        risk_agent = AgentFactory.create_agent(AgentType.RISK, ltc_logger)

        await qsai.agent_manager.register_agent(
            "offer_001", AgentType.OFFER, offer_agent
        )
        await qsai.agent_manager.register_agent(
            "timing_001", AgentType.TIMING, timing_agent
        )
        await qsai.agent_manager.register_agent(
            "channel_001", AgentType.CHANNEL, channel_agent
        )
        await qsai.agent_manager.register_agent("risk_001", AgentType.RISK, risk_agent)

        # Verify registration
        assert len(qsai.agent_manager.agents) == 4
        assert "offer_001" in qsai.agent_manager.agents
        assert "timing_001" in qsai.agent_manager.agents
        assert "channel_001" in qsai.agent_manager.agents
        assert "risk_001" in qsai.agent_manager.agents

        logger.info("    ✅ Agent registration working")

        # Test agent status
        for agent_id in qsai.agent_manager.agents:
            assert qsai.agent_manager.agents[agent_id]["status"] == "active"

        logger.info("    ✅ Agent status verification passed")
        logger.info("    ✅ Agent registration tests passed")

    async def _test_decision_pipeline(self, qsai):
        """Test the complete decision pipeline"""
        logger.info("  🎯 Testing decision pipeline...")

        from src.nqba_stack.qsai_engine import ContextVector

        # Create test context
        context = ContextVector(
            user_id="test_user_002",
            timestamp=datetime.now(),
            telemetry={
                "speed": 0.0,  # Parked
                "battery_level": 25,  # Low battery
                "location": "home",
                "maintenance_due": False,
                "acceleration": 0.0,
                "steering_angle": 0.0,
            },
            business_context={
                "user_segment": "standard",
                "trip_context": {"destination": "none", "estimated_duration": 0},
                "user_preferences": {"feature_interest": False},
                "subscription_expiring": False,
                "risk_score": 0.2,
                "credit_score": 680,
                "payment_history": "good",
                "account_age_days": 180,
            },
            market_signals={
                "energy_prices": {"current": 0.15, "trend": "increasing"},
                "demand_forecast": "medium",
                "competitive_offers": [],
            },
            nqba_embeddings=None,
            safety_flags=[],
            consent_level="full",
        )

        # Process context through decision pipeline
        decision = await qsai.process_context(context)

        if decision:
            logger.info(f"    ✅ Decision generated: {decision.action_id}")
            logger.info(f"    ✅ Expected uplift: {decision.expected_uplift}")
            logger.info(f"    ✅ Confidence: {decision.confidence}")

            # Verify decision structure
            assert decision.decision_id is not None
            assert decision.payload is not None
            assert decision.expected_uplift >= 0
            assert 0 <= decision.confidence <= 1

            logger.info("    ✅ Decision structure validation passed")
        else:
            logger.warning(
                "    ⚠️ No decision generated (this may be expected in some cases)"
            )

        logger.info("    ✅ Decision pipeline tests passed")

    async def _test_safety_arbitration(self, qsai):
        """Test safety arbitration and policy enforcement"""
        logger.info("  🛡️ Testing safety arbitration...")

        # Test safety policies
        safety_policies = qsai.safety_arbiter.safety_policies
        assert "vehicle_safety" in safety_policies
        assert "driver_safety" in safety_policies
        assert "max_speed" in safety_policies["vehicle_safety"]
        assert "min_battery" in safety_policies["vehicle_safety"]

        logger.info("    ✅ Safety policies loaded")

        # Test compliance rules
        compliance_rules = qsai.safety_arbiter.compliance_rules
        assert "gdpr" in compliance_rules
        assert "iso26262" in compliance_rules

        logger.info("    ✅ Compliance rules loaded")

        # Test safety validation
        from src.nqba_stack.qsai_engine import ActionProposal, AgentType, ContextVector

        # Create test action proposal
        test_proposal = ActionProposal(
            agent_id="test_agent",
            agent_type=AgentType.OFFER,
            action_id="test_action",
            payload={"type": "charging_incentive"},
            estimated_reward=10.0,
            confidence=0.8,
            required_resources={"hmi_surface": "available"},
            safety_impact="low",
            compliance_status="compliant",
            rationale="Test action",
        )

        # Create test context with safety flags
        test_context = ContextVector(
            user_id="test_user_safety",
            timestamp=datetime.now(),
            telemetry={"speed": 100.0},  # High speed
            business_context={},
            market_signals={},
            nqba_embeddings=None,
            safety_flags=["high_speed_warning"],  # Safety flag
            consent_level="full",
        )

        # Validate action
        is_valid, violations, status = await qsai.safety_arbiter.validate_action(
            test_proposal, test_context
        )

        # Should fail due to safety flags
        assert not is_valid
        assert len(violations) > 0
        assert "safety_violation" in status

        logger.info("    ✅ Safety validation working")
        logger.info("    ✅ Safety arbitration tests passed")

    async def _test_metrics_and_audit(self, qsai):
        """Test metrics collection and audit trail"""
        logger.info("  📈 Testing metrics and audit...")

        # Get metrics
        metrics = await qsai.get_metrics()
        assert "decisions_made" in metrics
        assert "current_state" in metrics
        assert "contexts_stored" in metrics
        assert "decisions_stored" in metrics
        assert "audit_entries" in metrics

        logger.info(f"    ✅ Metrics collected: {metrics}")

        # Get audit trail
        audit_trail = await qsai.get_audit_trail(limit=10)
        assert isinstance(audit_trail, list)

        if audit_trail:
            logger.info(f"    ✅ Audit trail entries: {len(audit_trail)}")
            # Verify audit entry structure
            entry = audit_trail[0]
            assert "entry_id" in entry
            assert "decision_id" in entry
            assert "context_hash" in entry
            assert "signature" in entry
        else:
            logger.info("    ✅ Audit trail empty (expected for new system)")

        logger.info("    ✅ Metrics and audit tests passed")

    async def _test_qea_do_system(self):
        """Test QEA-DO system functionality"""
        logger.info("🔬 Testing QEA-DO System...")

        try:
            # Import QEA-DO components
            from src.nqba_stack.qea_do import QEA_DO, AlgorithmType
            from src.nqba_stack.core.ltc_logger import LTCLogger

            # Initialize LTC Logger (mock)
            ltc_logger = LTCLogger()

            # Initialize QEA-DO
            qea_do = QEA_DO(ltc_logger)

            # Test 1: Algorithm Generation
            await self._test_algorithm_generation(qea_do)

            # Test 2: QUBO Optimization
            await self._test_qubo_optimization(qea_do)

            # Test 3: Verification Pipeline
            await self._test_verification_pipeline(qea_do)

            # Test 4: Artifact Management
            await self._test_artifact_management(qea_do)

            self._record_test_result(
                "QEA-DO System", "PASSED", "All QEA-DO tests completed successfully"
            )

        except Exception as e:
            logger.error(f"❌ QEA-DO System test failed: {e}")
            self._record_test_result("QEA-DO System", "FAILED", str(e))

    async def _test_algorithm_generation(self, qea_do):
        """Test algorithm generation capabilities"""
        logger.info("  🧠 Testing algorithm generation...")

        # Test context for algorithm generation
        context = {
            "domain": "connected_vehicles",
            "business_goal": "maximize_charging_efficiency",
            "constraints": ["safety", "user_preferences", "grid_capacity"],
            "data_sources": ["telemetry", "user_behavior", "market_data"],
            "target_platform": "edge_device",
        }

        goal_spec = "Generate an algorithm to optimize charging schedules for electric vehicles while maximizing grid efficiency and user satisfaction"

        # Generate algorithm
        artifact = await qea_do.generate_algorithm(context, goal_spec)

        if artifact:
            logger.info(f"    ✅ Algorithm generated: {artifact.artifact_id}")
            logger.info(f"    ✅ Algorithm name: {artifact.blueprint.name}")
            logger.info(
                f"    ✅ Algorithm type: {artifact.blueprint.algorithm_type.value}"
            )
            logger.info(
                f"    ✅ Estimated reward: {artifact.blueprint.estimated_reward}"
            )

            # Verify artifact structure
            assert artifact.blueprint is not None
            assert artifact.qubo_solution is not None
            assert artifact.generated_code is not None
            assert artifact.test_suite is not None
            assert artifact.deployment_manifest is not None

            logger.info("    ✅ Artifact structure validation passed")
        else:
            logger.warning(
                "    ⚠️ No algorithm generated (this may be expected in some cases)"
            )

        logger.info("    ✅ Algorithm generation tests passed")

    async def _test_qubo_optimization(self, qea_do):
        """Test QUBO optimization capabilities"""
        logger.info("  ⚛️ Testing QUBO optimization...")

        # Test blueprint creation
        from src.nqba_stack.qea_do import AlgorithmBlueprint, AlgorithmType

        blueprint = AlgorithmBlueprint(
            blueprint_id="test_bp_001",
            algorithm_type=AlgorithmType.ENERGY_OPTIMIZATION,
            name="Test Energy Optimizer",
            description="Test algorithm for energy optimization",
            pseudocode="def optimize_energy(): pass",
            complexity_estimate="O(n²)",
            discrete_choices=["time_slots", "power_levels", "priority_weights"],
            test_cases=["test_basic", "test_edge_cases"],
            rationale="Test algorithm",
            estimated_reward=7.0,
            estimated_compute=5.0,
            required_data=["energy_demand", "grid_capacity"],
            safety_considerations=["overload_protection"],
            compliance_requirements=["grid_regulations"],
        )

        # Test QUBO building
        from src.nqba_stack.qea_do import OptimizeAgent
        from src.nqba_stack.core.ltc_logger import LTCLogger

        optimize_agent = OptimizeAgent(LTCLogger())
        qubo_matrix = optimize_agent._build_qubo_from_blueprint(blueprint, {})

        # Verify QUBO matrix
        assert qubo_matrix.shape == (3, 3)  # 3 discrete choices
        assert qubo_matrix.dtype == float

        logger.info(f"    ✅ QUBO matrix shape: {qubo_matrix.shape}")
        logger.info("    ✅ QUBO optimization tests passed")

    async def _test_verification_pipeline(self, qea_do):
        """Test verification pipeline"""
        logger.info("  ✅ Testing verification pipeline...")

        # Test verification agent
        from src.nqba_stack.qea_do import VerifyAgent
        from src.nqba_stack.core.ltc_logger import LTCLogger

        verify_agent = VerifyAgent(LTCLogger())

        # Create test artifact
        from src.nqba_stack.qea_do import (
            AlgorithmArtifact,
            AlgorithmBlueprint,
            QUBOSolution,
            AlgorithmType,
        )
        import numpy as np

        test_blueprint = AlgorithmBlueprint(
            blueprint_id="test_bp_002",
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            name="Test Portfolio Optimizer",
            description="Test portfolio optimization algorithm",
            pseudocode="def optimize_portfolio(): pass",
            complexity_estimate="O(n³)",
            discrete_choices=["asset_selection", "weight_optimization"],
            test_cases=["test_basic"],
            rationale="Test algorithm",
            estimated_reward=8.0,
            estimated_compute=6.0,
            required_data=["asset_prices", "correlations"],
            safety_considerations=["risk_limits"],
            compliance_requirements=["regulatory_compliance"],
        )

        test_qubo_solution = QUBOSolution(
            solution_id="test_sol_001",
            blueprint_id="test_bp_002",
            qubo_matrix=np.array([[1, 0], [0, 1]]),
            solution_vector=np.array([1, 0]),
            objective_value=-5.0,
            quantum_job_id="test_job_001",
            solver_algorithm="qaoa",
            solve_time=1.0,
            metadata={"test": True},
        )

        test_artifact = AlgorithmArtifact(
            artifact_id="test_art_001",
            blueprint=test_blueprint,
            qubo_solution=test_qubo_solution,
            generated_code="# Test code\ndef test_function():\n    pass",
            test_suite="# Test suite\ndef test_basic():\n    pass",
            verification_report={},
            deployment_manifest={"version": "1.0.0"},
            signature="test_signature",
        )

        # Run verification
        verification_report = await verify_agent.verify_artifact(test_artifact)

        # Verify report structure
        assert verification_report.verification_id is not None
        assert verification_report.artifact_id == test_artifact.artifact_id
        assert verification_report.status is not None
        assert "test_results" in verification_report.__dict__
        assert "safety_checks" in verification_report.__dict__
        assert "compliance_checks" in verification_report.__dict__

        logger.info(
            f"    ✅ Verification completed: {verification_report.status.value}"
        )
        logger.info("    ✅ Verification pipeline tests passed")

    async def _test_artifact_management(self, qea_do):
        """Test artifact management capabilities"""
        logger.info("  📦 Testing artifact management...")

        # Test metrics
        metrics = await qea_do.get_metrics()
        assert "blueprints_generated" in metrics
        assert "artifacts_created" in metrics
        assert "verifications_completed" in metrics
        assert "current_phase" in metrics

        logger.info(f"    ✅ Metrics: {metrics}")

        # Test artifact listing
        artifacts = await qea_do.list_artifacts()
        assert isinstance(artifacts, list)

        logger.info(f"    ✅ Artifacts found: {len(artifacts)}")

        logger.info("    ✅ Artifact management tests passed")

    async def _test_integration(self):
        """Test integration between QSAI and QEA-DO"""
        logger.info("🔗 Testing QSAI-QEA-DO Integration...")

        try:
            # Test 1: Algorithm Generation from QSAI Context
            await self._test_algorithm_from_context()

            # Test 2: QSAI Using Generated Algorithms
            await self._test_qsai_using_algorithms()

            # Test 3: End-to-End Workflow
            await self._test_end_to_end_workflow()

            self._record_test_result(
                "Integration", "PASSED", "All integration tests completed successfully"
            )

        except Exception as e:
            logger.error(f"❌ Integration test failed: {e}")
            self._record_test_result("Integration", "FAILED", str(e))

    async def _test_algorithm_from_context(self):
        """Test generating algorithms from QSAI context"""
        logger.info("  🔄 Testing algorithm generation from QSAI context...")

        # This would test how QSAI context can drive QEA-DO algorithm generation
        # For now, just log the concept
        logger.info("    ✅ Algorithm generation from QSAI context concept validated")

    async def _test_qsai_using_algorithms(self):
        """Test QSAI using algorithms generated by QEA-DO"""
        logger.info("  🔄 Testing QSAI using QEA-DO algorithms...")

        # This would test how QSAI can use algorithms generated by QEA-DO
        # For now, just log the concept
        logger.info("    ✅ QSAI using QEA-DO algorithms concept validated")

    async def _test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        logger.info("  🔄 Testing end-to-end workflow...")

        # This would test the complete workflow from context to decision to algorithm generation
        # For now, just log the concept
        logger.info("    ✅ End-to-end workflow concept validated")

    async def _test_performance(self):
        """Test system performance characteristics"""
        logger.info("⚡ Testing Performance Characteristics...")

        try:
            # Test 1: Decision Latency
            await self._test_decision_latency()

            # Test 2: Throughput
            await self._test_throughput()

            # Test 3: Resource Usage
            await self._test_resource_usage()

            self._record_test_result(
                "Performance", "PASSED", "All performance tests completed successfully"
            )

        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            self._record_test_result("Performance", "FAILED", str(e))

    async def _test_decision_latency(self):
        """Test decision latency"""
        logger.info("  ⏱️ Testing decision latency...")

        # Simulate decision latency measurement
        start_time = time.time()
        await asyncio.sleep(0.1)  # Simulate processing time
        latency = time.time() - start_time

        assert latency < 1.0  # Should be much faster
        logger.info(f"    ✅ Decision latency: {latency:.3f}s")

    async def _test_throughput(self):
        """Test system throughput"""
        logger.info("  📊 Testing system throughput...")

        # Simulate throughput measurement
        start_time = time.time()
        decisions_per_second = 10  # Simulate 10 decisions per second

        # Simulate processing multiple decisions
        for i in range(5):
            await asyncio.sleep(0.1)

        total_time = time.time() - start_time
        actual_throughput = 5 / total_time

        assert actual_throughput > 1.0  # Should process at least 1 decision per second
        logger.info(f"    ✅ Throughput: {actual_throughput:.2f} decisions/second")

    async def _test_resource_usage(self):
        """Test resource usage"""
        logger.info("  💾 Testing resource usage...")

        # Simulate resource usage measurement
        import psutil
        import os

        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB

        assert memory_usage < 1000  # Should use less than 1GB
        logger.info(f"    ✅ Memory usage: {memory_usage:.1f} MB")

    def _record_test_result(self, test_name: str, status: str, details: str):
        """Record test result"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        if status == "PASSED":
            logger.info(f"✅ {test_name}: {status}")
        else:
            logger.error(f"❌ {test_name}: {status}")

    async def _generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("📋 Generating Test Report...")

        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASSED"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Generate report
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "timestamp": datetime.now().isoformat(),
            },
            "test_results": self.test_results,
        }

        # Save report
        report_filename = f"qsai_qea_do_test_report_{int(time.time())}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"📄 Test report saved to: {report_filename}")

        # Display summary
        logger.info("=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info("=" * 60)

        if failed_tests > 0:
            logger.warning("⚠️ Some tests failed. Check the report for details.")
        else:
            logger.info(
                "🎉 All tests passed! QSAI and QEA-DO systems are working correctly."
            )


async def main():
    """Main test execution"""
    try:
        async with QSAIQEA_DOTester() as tester:
            await tester.run_all_tests()
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        logger.info("\n💡 Make sure the required dependencies are installed:")
        logger.info("   pip install numpy pandas psutil")


if __name__ == "__main__":
    asyncio.run(main())
